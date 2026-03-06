# Nanobot 完整技术架构拆解

> 来源: https://github.com/HKUDS/nanobot
> 版本: v0.1.4.post3 (2026-02-28)
> 定位: 超轻量级个人 AI 助手框架
> 总代码: ~11,288 行 Python | 核心 Agent: 4,100 行

---

## 一、项目全景

### 1.1 核心理念

Nanobot 是香港大学数据科学实验室 (HKUDS) 开源的个人 AI 助手框架，灵感来自 OpenClaw，核心目标是：

- **极简**: 核心 Agent 仅 4,100 行 Python，是 OpenClaw 的 ~1%
- **研究友好**: 代码清晰可读，模块解耦，适合学术实验和二次开发
- **多渠道**: 一套 Agent 接入 12 个消息平台（含国内飞书/钉钉/QQ）
- **LLM 无关**: 通过 LiteLLM 统一适配 20+ 模型供应商

### 1.2 代码行数统计

```
模块                    行数
─────────────────────────────
agent/               1,335   # Agent 主循环 + 上下文 + 记忆 + 技能 + 子Agent
agent/tools/         1,215   # 工具层（文件/Shell/Web/Cron/MCP等）
bus/                    88   # 消息总线
config/                495   # Pydantic 配置 schema
cron/                  441   # 定时任务服务
heartbeat/             178   # 心跳服务
session/               217   # 会话持久化
utils/                 117   # 辅助函数
─────────────────────────────
核心合计            4,100 行  (不含 channels/ cli/ providers/)

channels/           ~3,500   # 12 个渠道实现
cli/                   938   # CLI 命令
providers/           ~1,750   # LLM Provider 层
─────────────────────────────
Python 总计       ~11,288 行
```

另有 Node.js/TypeScript WhatsApp Bridge ~500 行。

---

## 二、系统架构

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                        用户消息入口                                  │
│  Telegram│Discord│WhatsApp│飞书│钉钉│Slack│Email│Matrix│QQ│Mochat│CLI│
│  (各自实现 BaseChannel 接口)                                        │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ InboundMessage
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                   MessageBus (异步双向队列)                           │
│        inbound: asyncio.Queue[InboundMessage]                        │
│        outbound: asyncio.Queue[OutboundMessage]                      │
└──────────────┬──────────────────────────────────┬────────────────────┘
               │ consume_inbound()                 │ consume_outbound()
               ▼                                   ▼
┌──────────────────────────────┐    ┌──────────────────────────────────┐
│       AgentLoop (核心)        │    │     ChannelManager (路由分发)     │
│                              │    │                                  │
│  1. 加载 Session 历史         │    │  监听 outbound 队列              │
│  2. ContextBuilder 构建提示词  │    │  根据 msg.channel 分发到对应渠道  │
│  3. LLMProvider.chat() 调用   │    │  过滤 progress/tool_hint 消息    │
│  4. 解析 tool_calls           │    │                                  │
│  5. ToolRegistry.execute()    │    └──────────────────────────────────┘
│  6. 循环直到无 tool_call      │
│  7. 保存 Session              │
│  8. 触发 Memory Consolidation │
│  9. 发布 OutboundMessage      │
└──────────────────────────────┘
       ▲              │
       │              ▼
┌──────┴──────────────────────────────────────────────────────────────┐
│                     工具执行层 (ToolRegistry)                        │
│                                                                     │
│  内置工具:                                                          │
│  ┌────────────┬────────────┬────────────┬──────────────┐           │
│  │ read_file  │ write_file │ edit_file  │ list_dir     │           │
│  │ exec       │ web_search │ web_fetch  │ send_message │           │
│  │ cron       │ spawn_task │ MCP tools  │              │           │
│  └────────────┴────────────┴────────────┴──────────────┘           │
└─────────────────────────────────────────────────────────────────────┘

辅助服务:
┌─────────────┐  ┌────────────────┐  ┌───────────────────┐
│ CronService │  │ HeartbeatService│  │ SubagentManager  │
│ 定时任务调度 │  │ 30分钟心跳检查   │  │ 后台子Agent执行   │
└─────────────┘  └────────────────┘  └───────────────────┘
```

### 2.2 数据流详解

**完整请求生命周期:**

```
1. 用户在 Telegram 发送消息 "帮我查一下天气"
2. TelegramChannel.start() 收到消息 → is_allowed() 鉴权
3. BaseChannel._handle_message() → InboundMessage 入 MessageBus.inbound 队列
4. AgentLoop.run() 从队列消费 → asyncio.create_task(_dispatch(msg))
5. _dispatch() 获取 _processing_lock → _process_message()
6. SessionManager.get_or_create("telegram:12345") 加载历史
7. ContextBuilder.build_messages():
   - build_system_prompt(): identity + bootstrap + MEMORY.md + skills
   - 拼接 history + runtime_context + 用户消息
8. LiteLLMProvider.chat(messages, tools) → LLM 返回 tool_calls: [web_search]
9. ToolRegistry.execute("web_search", {"query": "北京天气"})
   → WebSearchTool 调用 Brave Search API → 返回结果
10. 结果追加到 messages，再次调用 LLM
11. LLM 返回纯文本回复（无 tool_calls），循环结束
12. _save_turn() 保存新消息到 Session
13. 检查是否需要 Memory Consolidation
14. OutboundMessage 发布到 MessageBus.outbound 队列
15. ChannelManager._dispatch_outbound() 消费 → TelegramChannel.send()
16. 用户收到回复
```

---

## 三、核心模块深度拆解

### 3.1 AgentLoop — 引擎核心

**文件**: `nanobot/agent/loop.py` (519 行)

AgentLoop 是整个系统的心脏，实现了经典的 ReAct (Reasoning + Acting) 循环。

**关键参数:**
```python
class AgentLoop:
    _TOOL_RESULT_MAX_CHARS = 500   # 工具结果截断长度
    max_iterations = 40             # 单次对话最大工具调用轮次
    memory_window = 100             # 触发记忆整合的消息阈值
    temperature = 0.1               # LLM 采样温度
    max_tokens = 4096               # LLM 最大输出 token
```

**核心方法:**

| 方法 | 职责 |
|------|------|
| `run()` | 主循环：消费消息队列、分发处理任务 |
| `_dispatch(msg)` | 获取全局锁 → 调用 _process_message → 发布响应 |
| `_process_message(msg)` | 完整消息处理：slash 命令 → 构建上下文 → Agent 循环 → 保存 |
| `_run_agent_loop(messages)` | 核心迭代循环：LLM → tool_calls → execute → 回传 → 重复 |
| `_save_turn(session, msgs)` | 保存新消息到 Session，截断长结果，去除运行时上下文 |
| `_consolidate_memory(session)` | 委托 MemoryStore 做记忆整合 |
| `process_direct(content)` | CLI/Cron 直接调用入口，绕过消息总线 |
| `_handle_stop(msg)` | 处理 /stop 命令：取消活跃任务 + 子Agent |

**关键设计决策:**

1. **全局处理锁** (`_processing_lock`): 确保同一时间只处理一条消息，避免并发修改 Session
2. **错误响应不持久化**: `finish_reason == "error"` 的 LLM 响应不写入 Session，防止上下文污染
3. **Tool 结果截断**: 超过 500 字符的工具结果在保存时被截断，节省上下文窗口
4. **运行时上下文剥离**: 保存 Session 时移除 `[Runtime Context]` 前缀，只保留纯用户文本
5. **空消息过滤**: 空的 assistant 消息不写入 Session，防止 API 报错

### 3.2 ContextBuilder — 提示词工程

**文件**: `nanobot/agent/context.py` (179 行)

负责将所有信息组装成 LLM 能理解的消息列表。

**System Prompt 结构:**
```
# nanobot 🐈
You are nanobot, a helpful AI assistant.
## Runtime
macOS arm64, Python 3.12.x
## Workspace
/path/to/workspace
## nanobot Guidelines
(行为准则)

---

## AGENTS.md
(代理指令: 定时任务使用指南、心跳任务管理等)

## SOUL.md
(人格设定: 友好、简洁、准确)

## USER.md
(用户自定义指令)

## TOOLS.md
(工具使用说明)

---

# Memory
## Long-term Memory
(MEMORY.md 内容)

---

# Active Skills
(always=true 的技能全文)

---

# Skills
(所有技能的 XML 摘要)
```

**消息列表结构:**
```python
[
    {"role": "system", "content": "<完整 system prompt>"},
    # ... Session 历史消息 (最多 memory_window 条) ...
    {"role": "user", "content": "[Runtime Context]\nCurrent Time: ...\nChannel: telegram\nChat ID: 12345\n\n用户实际消息"}
]
```

**多模态支持**: 当消息包含图片时，user content 变为 list 格式:
```python
[
    {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}},
    {"type": "text", "text": "这张图片是什么"}
]
```

### 3.3 MemoryStore — 三层记忆系统

**文件**: `nanobot/agent/memory.py` (158 行)

```
┌─────────────────────────────────────────────────────┐
│ 第一层: Session History (JSONL)                      │
│ 位置: workspace/sessions/{channel_chatid}.jsonl      │
│ 特点: 原始对话记录，append-only，支持 LLM 缓存      │
│ 用途: 短期上下文，直接喂给 LLM                       │
└─────────────────────────────────────────────────────┘
                    │ 当消息数 > memory_window (100)
                    ▼ LLM 驱动的 consolidation
┌─────────────────────────────────────────────────────┐
│ 第二层: MEMORY.md (长期记忆)                         │
│ 位置: workspace/memory/MEMORY.md                     │
│ 特点: Markdown 格式，人类可读可编辑                   │
│ 用途: 持久化的事实和知识，每次对话都注入 system prompt│
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 第三层: HISTORY.md (审计日志)                        │
│ 位置: workspace/memory/HISTORY.md                    │
│ 特点: 时间戳索引，grep 可搜索                        │
│ 格式: [YYYY-MM-DD HH:MM] ROLE [tools: X, Y]: 内容  │
│ 用途: 长期历史记录，Agent 可通过 grep 检索           │
└─────────────────────────────────────────────────────┘
```

**记忆整合流程 (Consolidation):**

```python
# 触发条件: 未整合消息数 >= memory_window (100)
# 执行方式: 异步任务 (不阻塞主循环)

1. 取出 session.messages[last_consolidated:-keep_count]
   (keep_count = memory_window // 2 = 50 条保留不动)

2. 格式化为文本摘要:
   "[2026-02-28 10:30] USER: 帮我查天气"
   "[2026-02-28 10:30] ASSISTANT [tools: web_search]: 北京今天多云..."

3. 拼接当前 MEMORY.md 内容，构建 consolidation prompt

4. 调用 LLM (带 save_memory 工具定义)
   LLM 必须调用 save_memory(history_entry=..., memory_update=...)

5. 将 history_entry 追加到 HISTORY.md
6. 将 memory_update 写入 MEMORY.md
7. 更新 session.last_consolidated 指针
```

**设计亮点:**
- **LLM 驱动**: 记忆整合由 LLM 完成，而非简单截断，保留语义信息
- **虚拟工具调用**: 强制 LLM 通过 `save_memory` 工具返回结构化数据，避免解析自由文本
- **Append-only Session**: 原始消息永不修改，保证 LLM prompt caching 有效
- **双写策略**: MEMORY.md (状态) + HISTORY.md (日志) 分别服务不同需求

### 3.4 ToolRegistry — 工具系统

**文件**: `nanobot/agent/tools/base.py` (107 行) + `registry.py` (67 行)

**Tool 抽象基类:**
```python
class Tool(ABC):
    @property
    def name(self) -> str: ...        # 工具名 (LLM 调用时用)
    @property
    def description(self) -> str: ... # 工具描述 (LLM 理解用途)
    @property
    def parameters(self) -> dict: ... # JSON Schema 参数定义
    async def execute(self, **kwargs) -> str: ... # 执行
    def validate_params(self, params) -> list[str]: ... # 参数校验
    def to_schema(self) -> dict: ...  # 转 OpenAI function calling 格式
```

**ToolRegistry 执行流程:**
```
1. tool = _tools.get(name) → 找不到返回错误 + 可用工具列表
2. tool.validate_params(params) → 校验 JSON Schema
3. result = await tool.execute(**params) → 异步执行
4. 如果结果以 "Error" 开头 → 追加 "[Analyze the error and try a different approach.]"
5. 返回结果给 Agent Loop
```

### 3.5 内置工具清单

| 工具 | 文件 | 行数 | 功能 |
|------|------|------|------|
| `read_file` | filesystem.py | ~60 | 读文件 (自动检测图片/媒体) |
| `write_file` | filesystem.py | ~40 | 写文件 (可选 append 模式) |
| `edit_file` | filesystem.py | ~80 | 按行号范围替换内容 |
| `list_dir` | filesystem.py | ~50 | 列出目录内容 (含大小/权限) |
| `exec` | shell.py | 159 | Shell 命令执行 (带安全守卫) |
| `web_search` | web.py | ~60 | Brave Search API 搜索 |
| `web_fetch` | web.py | ~80 | 网页抓取 + readability 提取 |
| `send_message` | message.py | ~40 | 跨渠道发消息 |
| `cron` | cron.py | ~120 | 定时任务 add/list/remove |
| `spawn_task` | spawn.py | ~30 | 创建后台子Agent |
| + MCP tools | mcp.py | ~100 | 动态注册的 MCP 工具 |

**Shell 安全守卫 (ExecTool):**
```python
deny_patterns = [
    r"\brm\s+-[rf]{1,2}\b",          # rm -rf
    r"\bdel\s+/[fq]\b",              # Windows del
    r"\brmdir\s+/s\b",               # Windows rmdir
    r"(?:^|[;&|]\s*)format\b",       # format 命令
    r"\b(mkfs|diskpart)\b",          # 磁盘操作
    r"\bdd\s+if=",                   # dd
    r">\s*/dev/sd",                  # 写磁盘
    r"\b(shutdown|reboot|poweroff)\b", # 系统电源
    r":\(\)\s*\{.*\};\s*:",          # fork bomb
]
```

当 `restrict_to_workspace=True` 时，额外检查:
- `../` 路径遍历阻断
- 绝对路径必须在 workspace 目录内

### 3.6 Provider 系统 — LLM 适配层

**架构:**
```
                        Config._match_provider()
                              │
                    ┌─────────┼──────────┐
                    ▼         ▼          ▼
            CustomProvider  LiteLLMProvider  OpenAICodexProvider
            (直连OpenAI兼容)  (20+供应商)     (OAuth)
                    │         │              │
                    ▼         ▼              ▼
              OpenAI SDK    LiteLLM SDK    oauth_cli_kit
```

**Provider Registry (`providers/registry.py`, 439 行):**

采用声明式数据驱动设计，每个 Provider 只需一个 `ProviderSpec` 数据类:

```python
@dataclass(frozen=True)
class ProviderSpec:
    name: str                   # 配置字段名 ("dashscope")
    keywords: tuple[str, ...]   # 模型名匹配关键词 ("qwen", "dashscope")
    env_key: str                # LiteLLM 环境变量 ("DASHSCOPE_API_KEY")
    display_name: str           # 显示名
    litellm_prefix: str         # LiteLLM 前缀 ("dashscope" → "dashscope/qwen-max")
    skip_prefixes: tuple        # 避免重复前缀
    env_extras: tuple           # 额外环境变量
    is_gateway: bool            # 是否为网关型 (OpenRouter, AiHubMix)
    is_local: bool              # 是否本地部署 (vLLM)
    is_oauth: bool              # 是否 OAuth 认证
    is_direct: bool             # 是否直连 (绕过 LiteLLM)
    supports_prompt_caching: bool # 支持 prompt caching
    detect_by_key_prefix: str   # API key 前缀自动检测
    detect_by_base_keyword: str # API base URL 关键词检测
    model_overrides: tuple      # 模型级参数覆盖
```

**支持的 Provider (16个):**

| 类型 | Provider | 特点 |
|------|----------|------|
| 网关 | OpenRouter | 全球网关，`sk-or-` key 自动检测 |
| 网关 | AiHubMix | OpenAI 兼容，`strip_model_prefix=True` |
| 网关 | SiliconFlow | 硅基流动 |
| 网关 | VolcEngine | 火山引擎 |
| 直连 | Anthropic | 原生支持 prompt caching |
| 直连 | OpenAI | `gpt-*` 自动识别 |
| 直连 | DeepSeek | `deepseek/` 前缀 |
| 直连 | Gemini | `gemini/` 前缀 |
| 直连 | Zhipu | `zai/` 前缀，双环境变量 |
| 直连 | DashScope | 阿里云通义千问 |
| 直连 | Moonshot | Kimi，温度覆盖 >=1.0 |
| 直连 | MiniMax | `minimax/` 前缀 |
| 直连 | Groq | 语音转写 + LLM |
| 本地 | vLLM | `hosted_vllm/` 前缀 |
| 自定义 | Custom | 绕过 LiteLLM 直连 |
| OAuth | OpenAI Codex / GitHub Copilot | OAuth 设备流认证 |

**新增 Provider 只需 2 步:**
1. 在 `registry.py` 添加 `ProviderSpec` (~10 行)
2. 在 `schema.py` 的 `ProvidersConfig` 添加字段 (1 行)

**LiteLLMProvider 核心流程:**
```python
async def chat(messages, tools, model, ...):
    # 1. 模型名解析: 自动添加 provider 前缀
    model = self._resolve_model(original_model)  # "claude-3" → "openrouter/claude-3"

    # 2. Prompt Caching: 对支持的 provider 注入 cache_control
    if self._supports_cache_control(model):
        messages, tools = self._apply_cache_control(messages, tools)

    # 3. 消息净化: 去除非标准 key，处理空内容
    messages = self._sanitize_messages(self._sanitize_empty_content(messages))

    # 4. 模型级覆盖: 如 Kimi K2.5 强制 temperature >= 1.0
    self._apply_model_overrides(model, kwargs)

    # 5. 调用 LiteLLM
    response = await acompletion(**kwargs)

    # 6. 解析响应: 统一格式化 tool_calls, reasoning_content, thinking_blocks
    return self._parse_response(response)
```

### 3.7 消息总线 (MessageBus)

**文件**: `nanobot/bus/queue.py` (45 行) + `events.py` (38 行)

极简的异步双队列设计:

```python
class MessageBus:
    inbound: asyncio.Queue[InboundMessage]   # 渠道 → Agent
    outbound: asyncio.Queue[OutboundMessage]  # Agent → 渠道

class InboundMessage:
    channel: str       # "telegram"
    sender_id: str     # "12345"
    chat_id: str       # "12345" (私聊) 或 群组ID
    content: str       # 消息文本
    media: list[str]   # 附件路径列表
    metadata: dict     # 渠道特有数据 (message_id 等)
    session_key_override: str | None  # 线程隔离 key

    @property
    def session_key(self) -> str:  # "telegram:12345"
        return self.session_key_override or f"{self.channel}:{self.chat_id}"
```

### 3.8 Session 管理

**文件**: `nanobot/session/manager.py` (213 行)

**存储格式: JSONL**
```
{"_type": "metadata", "key": "telegram:12345", "created_at": "...", "last_consolidated": 50}
{"role": "user", "content": "你好", "timestamp": "2026-02-28T10:00:00"}
{"role": "assistant", "content": "你好！", "tool_calls": [...], "timestamp": "..."}
{"role": "tool", "tool_call_id": "abc123", "name": "web_search", "content": "..."}
```

**设计要点:**
- **Append-only**: 消息只追加不修改，配合 LLM prompt caching
- **内存缓存**: `_cache: dict[str, Session]` 避免重复读盘
- **Legacy 迁移**: 自动将 `~/.nanobot/sessions/` 迁移到 workspace
- **历史对齐**: `get_history()` 从 `last_consolidated` 开始，跳过前导非 user 消息，避免孤立的 tool_result

### 3.9 Channel 系统

**文件**: `nanobot/channels/base.py` (120 行) + `manager.py` (256 行)

**BaseChannel 接口:**
```python
class BaseChannel(ABC):
    name: str = "base"

    async def start(self) -> None: ...    # 连接平台，监听消息
    async def stop(self) -> None: ...     # 断开连接
    async def send(self, msg) -> None: ... # 发送消息
    def is_allowed(self, sender_id) -> bool: ... # 鉴权

    async def _handle_message(self, sender_id, chat_id, content, ...):
        # 统一入口: 鉴权 → 构造 InboundMessage → 入队
```

**ChannelManager 职责:**
1. 根据 config 初始化已启用的渠道 (lazy import，缺失依赖不崩溃)
2. 验证 `allowFrom` 非空 (空列表会拒绝所有人)
3. 并行启动所有渠道
4. 运行 outbound dispatcher: 从队列消费 → 路由到对应渠道的 `send()`
5. 过滤 progress / tool_hint 消息

**各渠道实现概览:**

| 渠道 | 协议 | 库 | 特殊功能 |
|------|------|---|---------|
| Telegram | Bot API (Polling) | python-telegram-bot | 语音转写 (Groq Whisper) |
| Discord | WebSocket Gateway v10 | 自实现 | typing 状态, 长消息拆分 |
| WhatsApp | WebSocket Bridge | Baileys (Node.js) | QR 扫码配对, 消息去重 |
| 飞书 | WebSocket 长连接 | lark-oapi | 富文本 Post, 表格拆分 |
| 钉钉 | Stream Mode | dingtalk-stream | 媒体消息支持 |
| Slack | Socket Mode | slack-sdk | 线程隔离, mrkdwn 格式 |
| Email | IMAP + SMTP | 标准库 | 轮询收件, 自动回复 |
| Matrix | HTTP API | matrix-nio | E2EE 加密支持 |
| QQ | WebSocket | qq-botpy | 仅私聊 |
| Mochat | Socket.IO | python-socketio | 多Session/Panel |
| CLI | stdin/stdout | prompt-toolkit | 交互模式 + 单消息模式 |

### 3.10 Skills 技能系统

**文件**: `nanobot/agent/skills.py` (229 行)

**技能结构:**
```
workspace/skills/
└── weather/
    └── SKILL.md
```

**SKILL.md 格式:**
```yaml
---
description: "Weather API queries"
metadata: '{"nanobot": {"always": false, "requires": {"bins": ["curl"], "env": ["WEATHER_API_KEY"]}}}'
---

# Weather Skill

Use this skill to query weather information...
```

**加载策略 (渐进式):**
1. **Always-on 技能**: `always: true` 的技能全文注入 system prompt
2. **摘要列表**: 所有技能的 XML 摘要放入 prompt，包含名称、描述、路径、可用状态
3. **按需加载**: Agent 调用 `read_file` 读取 SKILL.md 获取完整指令

**技能优先级**: Workspace skills > Builtin skills (同名覆盖)

**内置技能 (9个):**
- `memory`: 记忆管理
- `github`: GitHub CLI 集成
- `weather`: 天气 API
- `clawhub`: 社区技能市场搜索/安装
- `tmux`: 终端复用器控制
- `cron`: 定时任务 UI
- `skill-creator`: 自动生成新技能
- `summarize`: 文本摘要

### 3.11 SubagentManager — 子Agent

**文件**: `nanobot/agent/subagent.py` (247 行)

```
主 Agent                           子 Agent (后台)
   │                                  │
   │ spawn_task("分析这份报告")        │
   │────────────────────────────────>│
   │                                  │ 独立工具集 (无 message/spawn)
   │ "已启动子任务..."                 │ 最多 15 轮迭代
   │                                  │ ...工具调用...
   │                                  │
   │                                  │ 完成
   │<─── InboundMessage (system) ────│
   │ "[Subagent 'xxx' completed]"     │
   │                                  │
   │ 主 Agent 总结结果 → 回复用户     │
```

**限制:**
- 子 Agent 无法发消息 (防止直接干扰用户)
- 子 Agent 无法再 spawn (防止无限递归)
- 最多 15 轮迭代 (主 Agent 是 40 轮)
- 结果通过 system channel 注入主 Agent

### 3.12 CronService — 定时任务

**文件**: `nanobot/cron/service.py` (377 行)

支持三种调度模式:
1. **`at`**: 一次性定时 (指定毫秒时间戳)
2. **`every`**: 周期重复 (间隔毫秒)
3. **`cron`**: Cron 表达式 (支持时区)

**数据模型:**
```python
CronJob:
    id: str                    # 8位 UUID
    name: str                  # 任务名
    enabled: bool
    schedule: CronSchedule     # kind + at_ms/every_ms/expr/tz
    payload: CronPayload       # message + deliver + channel + to
    state: CronJobState        # next_run_at_ms + last_run_at_ms + last_status
    delete_after_run: bool     # 一次性任务自动删除
```

**存储**: `workspace/cron/jobs.json` (JSON, 支持外部修改热重载)

### 3.13 HeartbeatService — 心跳服务

**文件**: `nanobot/heartbeat/service.py` (174 行)

**两阶段设计:**

```
Phase 1: 决策 (轻量)
  ┌─ 每 30 分钟读取 HEARTBEAT.md
  ├─ 构建简短 prompt + heartbeat 虚拟工具
  ├─ LLM 调用 heartbeat(action="skip"|"run", tasks="...")
  └─ action == "skip" → 结束 | action == "run" → Phase 2

Phase 2: 执行 (完整)
  ┌─ 找到最近活跃的非 CLI 渠道
  ├─ agent.process_direct(tasks) → 完整 Agent 循环
  └─ 结果通过 on_notify() 发送到用户渠道
```

**核心设计**: 用虚拟工具调用代替文本匹配，100% 可靠的决策解析。

### 3.14 MCP (Model Context Protocol) 集成

**文件**: `nanobot/agent/tools/mcp.py`

```python
# 配置 (config.json):
{
    "tools": {
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
            },
            "remote-mcp": {
                "url": "https://example.com/mcp/",
                "headers": {"Authorization": "Bearer xxx"},
                "toolTimeout": 120
            }
        }
    }
}
```

**连接流程:**
1. Gateway 启动时 lazy 连接 (`_connect_mcp()`)
2. 通过 `AsyncExitStack` 管理 MCP 客户端生命周期
3. 发现每个 MCP server 提供的工具列表
4. 将 MCP 工具转换为 OpenAI function schema 注册到 ToolRegistry
5. 执行时通过 MCP 协议调用远程工具

**支持的传输:**
- **Stdio**: 本地进程 (npx/uvx 启动)
- **HTTP**: 远程端点 (SSE/StreamableHTTP)

---

## 四、配置系统

**文件**: `nanobot/config/schema.py` (421 行)

采用 Pydantic v2 + pydantic-settings，支持:
- JSON 配置文件 (`~/.nanobot/config.json`)
- 环境变量 (前缀 `NANOBOT_`, `__` 分隔嵌套)
- camelCase / snake_case 双向兼容

**配置层次:**
```python
Config
├── agents: AgentsConfig
│   └── defaults: AgentDefaults
│       ├── workspace: str = "~/.nanobot/workspace"
│       ├── model: str = "anthropic/claude-opus-4-5"
│       ├── provider: str = "auto"
│       ├── max_tokens: int = 8192
│       ├── temperature: float = 0.1
│       ├── max_tool_iterations: int = 40
│       ├── memory_window: int = 100
│       └── reasoning_effort: str | None
├── channels: ChannelsConfig
│   ├── send_progress: bool = True
│   ├── send_tool_hints: bool = False
│   ├── telegram: TelegramConfig
│   ├── discord: DiscordConfig
│   ├── whatsapp: WhatsAppConfig
│   ├── feishu: FeishuConfig
│   ├── dingtalk: DingTalkConfig
│   ├── slack: SlackConfig
│   ├── email: EmailConfig
│   ├── qq: QQConfig
│   ├── matrix: MatrixConfig
│   └── mochat: MochatConfig
├── providers: ProvidersConfig
│   ├── custom / anthropic / openai / openrouter / deepseek
│   ├── groq / zhipu / dashscope / vllm / gemini
│   ├── moonshot / minimax / aihubmix / siliconflow
│   ├── volcengine / openai_codex / github_copilot
│   └── (每个都是 ProviderConfig: api_key + api_base + extra_headers)
├── gateway: GatewayConfig
│   ├── host: str = "0.0.0.0"
│   ├── port: int = 18790
│   └── heartbeat: HeartbeatConfig (enabled + interval_s)
└── tools: ToolsConfig
    ├── web: WebToolsConfig (proxy + search)
    ├── exec: ExecToolConfig (timeout + path_append)
    ├── restrict_to_workspace: bool = False
    └── mcp_servers: dict[str, MCPServerConfig]
```

**Provider 自动匹配逻辑 (`Config._match_provider()`):**
```
1. 如果设置了 provider: "xxx" (非 "auto") → 直接使用
2. 模型名前缀精确匹配: "deepseek/chat" → deepseek provider
3. 关键词模糊匹配: "claude-3" 包含 "claude" → anthropic
4. 回退: 按 PROVIDERS 顺序找第一个有 api_key 的 (跳过 OAuth)
```

---

## 五、Workspace 文件结构

```
~/.nanobot/
├── config.json               # 全局配置
├── history/
│   └── cli_history           # CLI 交互历史 (prompt-toolkit)
├── bridge/                   # WhatsApp Bridge (Node.js, 按需构建)
│   ├── dist/index.js
│   └── auth_info/            # WhatsApp 认证数据
└── workspace/                # Agent 工作空间 (可自定义路径)
    ├── AGENTS.md             # Agent 指令 (bootstrap)
    ├── SOUL.md               # 人格设定 (bootstrap)
    ├── USER.md               # 用户自定义指令 (bootstrap)
    ├── TOOLS.md              # 工具说明 (bootstrap)
    ├── HEARTBEAT.md          # 心跳任务清单
    ├── memory/
    │   ├── MEMORY.md         # 长期记忆
    │   └── HISTORY.md        # 审计日志
    ├── sessions/
    │   ├── telegram_12345.jsonl
    │   ├── discord_67890.jsonl
    │   └── cli_direct.jsonl
    ├── skills/               # 用户自定义技能
    │   └── my-skill/
    │       └── SKILL.md
    └── cron/
        └── jobs.json         # 定时任务存储
```

---

## 六、部署架构

### 6.1 本地部署

```bash
pip install nanobot-ai    # 或 uv tool install nanobot-ai
nanobot onboard           # 初始化
# 编辑 ~/.nanobot/config.json 添加 API key
nanobot agent             # 交互模式
nanobot gateway           # 多渠道网关模式
```

### 6.2 Docker 部署

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
# 安装 Node.js 20 (WhatsApp Bridge)
# 两阶段构建: 先装依赖 (缓存层) → 再拷源码
# 构建 WhatsApp Bridge (npm install && build)
EXPOSE 18790
ENTRYPOINT ["nanobot"]
```

```yaml
# docker-compose.yml
services:
  nanobot-gateway:
    command: ["gateway"]
    ports: ["18790:18790"]
    volumes: ["~/.nanobot:/root/.nanobot"]
    deploy:
      resources:
        limits: { cpus: '1', memory: 1G }
        reservations: { memory: 256M }
```

### 6.3 systemd 服务

```ini
[Service]
ExecStart=%h/.local/bin/nanobot gateway
Restart=always
RestartSec=10
NoNewPrivileges=yes
ProtectSystem=strict
ReadWritePaths=%h
```

### 6.4 多实例部署

```bash
nanobot gateway -w ~/.nanobot/botA -p 18791  # 实例A
nanobot gateway -w ~/.nanobot/botB -p 18792  # 实例B
nanobot gateway -w ~/.nanobot/botC -c custom.json -p 18793  # 实例C
```

每个实例有独立的 workspace / session / cron / memory。

---

## 七、安全模型

| 层面 | 机制 | 详情 |
|------|------|------|
| **访问控制** | `allowFrom` 白名单 | 空列表 = 拒绝所有; `["*"]` = 允许所有 |
| **文件系统** | `restrict_to_workspace` | 限制所有工具到 workspace 目录 |
| **路径遍历** | `allowed_dir` 参数 | read/write/edit/list_dir 检查路径 |
| **Shell 执行** | 命令黑名单 (正则) | rm -rf, dd, mkfs, fork bomb 等 |
| **Shell 超时** | `timeout` 配置 | 默认 60 秒，可配置 |
| **工具结果** | 截断 500 字符 | 防止 Session 膨胀 |
| **Session 防护** | 错误响应不持久化 | 防止 400 循环 |
| **API Key** | config.json (0600) | 文件权限保护 |
| **WhatsApp Bridge** | localhost only | 127.0.0.1:3001，可选 token 认证 |
| **MCP 超时** | `toolTimeout` | 默认 30 秒，防止悬挂 |
| **Consolidation 锁** | `asyncio.Lock` per session | 防止并发整合竞态 |

---

## 八、测试体系

**框架**: Pytest + pytest-asyncio
**配置**: `asyncio_mode = "auto"` (所有 async 测试自动运行)

**测试覆盖 (16 个测试文件):**

| 测试文件 | 覆盖内容 |
|---------|---------|
| test_commands.py | CLI onboard/agent/status 命令 |
| test_cli_input.py | CLI 交互输入处理 |
| test_tool_validation.py | 工具参数 JSON Schema 校验 |
| test_memory_consolidation_types.py | 记忆整合参数类型处理 |
| test_consolidate_offset.py | consolidation 指针偏移 |
| test_context_prompt_cache.py | Prompt caching 注入 |
| test_loop_save_turn.py | Session 保存逻辑 |
| test_message_tool.py | 跨渠道消息工具 |
| test_message_tool_suppress.py | 消息工具抑制 |
| test_cron_service.py | Cron 调度逻辑 |
| test_heartbeat_service.py | 心跳决策/执行 |
| test_feishu_post_content.py | 飞书富文本 |
| test_feishu_table_split.py | 飞书表格拆分 |
| test_matrix_channel.py | Matrix 加密 |
| test_email_channel.py | Email 收发 |
| test_task_cancel.py | 任务取消 |

---

## 九、扩展指南

### 9.1 新增 LLM Provider (2 步)

```python
# 1. registry.py: 添加 ProviderSpec
ProviderSpec(
    name="myprovider",
    keywords=("myprovider",),
    env_key="MYPROVIDER_API_KEY",
    display_name="My Provider",
    litellm_prefix="myprovider",
    skip_prefixes=("myprovider/",),
)

# 2. schema.py: 添加配置字段
class ProvidersConfig(Base):
    myprovider: ProviderConfig = Field(default_factory=ProviderConfig)
```

### 9.2 新增工具

```python
class MyTool(Tool):
    @property
    def name(self) -> str: return "my_tool"

    @property
    def description(self) -> str: return "Does something useful"

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {"input": {"type": "string"}},
            "required": ["input"]
        }

    async def execute(self, input: str, **kwargs) -> str:
        return f"Result: {input}"

# 在 AgentLoop._register_default_tools() 中注册:
self.tools.register(MyTool())
```

### 9.3 新增消息渠道

```python
class MyChannel(BaseChannel):
    name = "mychannel"

    async def start(self):
        self._running = True
        # 连接平台，监听消息
        while self._running:
            msg = await self._receive()
            await self._handle_message(
                sender_id=msg.sender,
                chat_id=msg.chat,
                content=msg.text,
            )

    async def stop(self):
        self._running = False

    async def send(self, msg: OutboundMessage):
        await self._platform_send(msg.chat_id, msg.content)
```

### 9.4 新增技能 (零代码)

```markdown
<!-- workspace/skills/my-skill/SKILL.md -->
---
description: "我的自定义技能"
metadata: '{"nanobot": {"always": false, "requires": {"bins": ["curl"]}}}'
---

# My Skill

当用户要求 XXX 时，按以下步骤执行:
1. ...
2. ...
```

---

## 十、设计哲学总结

### 10.1 极简主义

- **核心仅 4,100 行**: 每个模块职责单一，无冗余抽象
- **无 ORM、无数据库**: 文件系统即存储 (JSONL + Markdown + JSON)
- **无 Web 框架**: 纯 asyncio，无 FastAPI/Flask 依赖
- **无状态机**: 简单的 while 循环 + if-else

### 10.2 数据驱动

- **Provider Registry**: 声明式 `ProviderSpec`，新增 Provider 只需填数据
- **Tool Schema**: OpenAI JSON Schema 标准，自动校验和转换
- **Skill Metadata**: YAML frontmatter，自动依赖检查
- **Config Schema**: Pydantic 声明式，自动验证 + 双命名风格

### 10.3 可观测性

- **MEMORY.md**: 人类可读的长期记忆
- **HISTORY.md**: grep 可搜索的完整历史
- **Session JSONL**: 逐行可读的对话记录
- **Loguru**: 结构化日志，按模块过滤
- **nanobot status**: 一览全局状态

### 10.4 研究友好

- **模块清晰解耦**: Agent Loop / Context / Memory / Tools / Channels 可独立实验
- **入口明确**: `AgentLoop._run_agent_loop()` 是核心 58 行，ReAct 循环一目了然
- **无黑盒**: 不依赖 LangChain/LlamaIndex 等重框架，每行代码都可追踪
- **热修改**: 技能系统 + Bootstrap 文件可运行时修改，无需重启
