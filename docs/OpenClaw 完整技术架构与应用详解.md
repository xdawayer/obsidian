# OpenClaw 完整技术架构与应用详解

> 创建日期: 2026-02-26
> 标签: #AI #OpenClaw #Agent编排 #技术架构 #Claude-Code #Codex

---

## 第一部分：OpenClaw 是什么

OpenClaw（曾用名 Clawdbot / Moltbot）是由 Peter Steinberger 开发的**开源自治 AI Agent 平台**（MIT 许可证），用 TypeScript 编写，2026 年 1 月爆火，GitHub 超 10 万星。

**核心定位**：它不是聊天机器人，而是一个**本地运行的 AI Agent 编排运行时**——一个能调度多个 AI 模型、执行真实操作、拥有持久记忆的"AI 管家"。

2026 年 2 月 14 日，Steinberger 宣布加入 OpenAI，项目将移交至开源基金会。

---

## 第二部分：核心架构 —— 三层设计

OpenClaw 采用**轴辐式（Hub-and-Spoke）三层架构**：

```
┌─────────────────────────────────────────────────────┐
│                   Channel 层（平台适配）               │
│  WhatsApp · Telegram · Slack · Discord · 飞书 · iMessage │
│  50+ 消息平台，统一归一化为 StandardMessage 格式         │
└──────────────────────┬──────────────────────────────┘
                       │ 归一化消息
┌──────────────────────▼──────────────────────────────┐
│                  Gateway 层（中央控制平面）             │
│  WebSocket 服务 · 会话管理 · 路由 · 认证 · 并发控制     │
│  消息队列 · 插件加载 · Cron 调度 · 健康监控              │
│  默认绑定: ws://127.0.0.1:18789                       │
└──────────────────────┬──────────────────────────────┘
                       │ 结构化上下文
┌──────────────────────▼──────────────────────────────┐
│              LLM Provider 层（可插拔模型接口）           │
│  Anthropic Claude · OpenAI · Gemini · DeepSeek · Ollama │
│  统一 Provider 接口，运行时动态注册，流式传输             │
└─────────────────────────────────────────────────────┘
```

### 2.1 Channel 层：50+ 消息平台适配

将不同平台的消息格式**归一化**为统一接口：

```typescript
interface StandardMessage {
  userId: string;       // 统一用户标识
  channelId: string;    // 平台+频道标识
  content: string;      // 消息文本
  timestamp: number;    // 时间戳
  metadata: any;        // 平台特有元数据
}
```

**平台差异被完全屏蔽**：WhatsApp 的 JID 转为 E.164 格式，Telegram 的 Username 转为稳定标识符，Discord 的 Snowflake ID 带上 guild/channel 上下文。Gateway 和 LLM 层完全不需要关心消息来自哪个平台。

**访问控制**：
- `pairing`（默认）：未知发送者获得 1 小时配对码，最多 3 个待定
- `allowlist`：白名单
- `open`：需显式配置 `"*"`
- `disabled`：拒绝所有

### 2.2 Gateway 层：系统的"大脑"

Gateway 是一个**单进程 Node.js 守护进程**，是整个系统的"交通管制中心 + 唯一真相源"。

**所有组件都连接到 Gateway**：Channel 适配器、CLI 工具、Web UI、iOS/Android 节点、外围设备——全部通过 WebSocket 通信。

#### WebSocket 协议

所有通信使用 JSON 文本帧，第一帧必须是 `connect` 握手请求：

| 帧类型 | 结构 | 方向 | 用途 |
|--------|------|------|------|
| Request | `{type:"req", id, method, params}` | 客户端→Gateway | 发起请求 |
| Response | `{type:"res", id, ok, payload}` | Gateway→客户端 | 返回结果 |
| Event | `{type:"event", event, payload, seq}` | Gateway→客户端 | 推送事件 |

#### 消息处理六阶段流水线

```
消息进入 → ① 摄入 → ② 访问控制 → ③ 会话解析 → ④ 上下文组装 → ⑤ 模型调用 → ⑥ 响应投递
```

1. **摄入**：平台适配器解析原始消息，提取文本/媒体/元数据
2. **访问控制**：白名单验证、DM 配对检查、群组 @提及过滤
3. **会话解析**：用层级键 `{scope}-{agentId}-{identifier}` 找到或创建会话
4. **上下文组装**：加载会话历史 + 构建系统提示词 + 语义搜索记忆
5. **模型调用**：流式发送到 LLM，拦截工具调用并执行
6. **响应投递**：格式化后通过适配器回流，持久化会话状态

#### 并发控制

**关键原则**："同一 Session 串行，不同 Session 并行。"

分布式部署使用 Redis redlock 分布式锁，防止同一用户的消息被并发处理导致上下文混乱。

#### 会话存储

会话持久化为 JSONL 文件：`~/.openclaw/sessions/{sessionId}.jsonl`，每行是一个 JSON 编码的 `AgentMessage` 对象。三层防护：工具结果截断、上下文窗口预防性压缩（80% 阈值）、会话修复。

### 2.3 LLM Provider 层：可插拔模型

使用统一的 `provider/model` 引用格式：

```
anthropic/claude-opus-4-6
openai/gpt-5.3
google/gemini-3-pro
deepseek/deepseek-r1
```

底层通过 **Pi Agent Core** 库抽象不同 API 协议差异：
- Claude：XML 风格 `tool_use` 块
- Gemini：`function_declaration` / `function_call`
- OpenAI：标准 function calling 格式

**密钥管理优先级链**（从高到低）：
1. `OPENCLAW_LIVE_<PROVIDER>_KEY`
2. `<PROVIDER>_API_KEYS`（逗号分隔多密钥，自动轮换）
3. `<PROVIDER>_API_KEY`

仅在遭遇**速率限制**时才轮换到下一个密钥。

---

## 第三部分：Agent 执行运行时 —— AI 如何"干活"

### 3.1 Agent 运行四阶段

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Phase 1      │    │ Phase 2      │    │ Phase 3      │    │ Phase 4      │
│ 上下文组装    │ →  │ 模型推理      │ →  │ 工具执行      │ →  │ 状态持久化    │
│              │    │              │    │              │    │              │
│ · 加载会话历史 │    │ · 流式传送    │    │ · 拦截工具调用 │    │ · 保存到JSONL │
│ · 构建系统提示 │    │   到Provider  │    │ · 沙箱内执行   │    │ · 更新记忆    │
│ · 查询记忆系统 │    │ · 增量接收    │    │ · 结果回传模型 │    │ · 触发通知    │
│ · 注入Skills  │    │   token      │    │ · 继续生成    │    │              │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

**Phase 1 上下文组装** 是关键。`buildAgentSystemPrompt()` 函数从工作区文件动态构建系统提示词：

| 文件 | 作用 | 限制 |
|------|------|------|
| `AGENTS.md` | 操作指令与行为规则 | 单文件 20,000 字符 |
| `SOUL.md` | 人格、语气、操作边界 | 总计 150,000 字符 |
| `USER.md` | 用户身份与偏好 | |
| `IDENTITY.md` | Agent 名称、性格特征 | |
| `TOOLS.md` | 本地工具使用指引 | |
| `HEARTBEAT.md` | 心跳检查清单 | |

还会注入运行时元数据：Host/OS/Node 版本、当前模型、仓库根路径。

### 3.2 工具系统（Function Calling）

OpenClaw 的工具分为六大组：

| 工具组 | 包含的工具 | 说明 |
|--------|-----------|------|
| `group:runtime` | `exec`, `bash`, `process` | Shell 命令执行、进程管理 |
| `group:fs` | `read`, `write`, `edit`, `apply_patch` | 文件读写编辑 |
| `group:web` | `web_search`, `web_fetch`, `image` | 网络搜索、网页抓取、图像分析 |
| `group:ui` | `browser`, `canvas` | 浏览器自动化（CDP 协议） |
| `group:messaging` | `message` | 跨平台消息收发 |
| `group:sessions` | `sessions_spawn`, `sessions_send` | 子 Agent 生成、Agent 间通信 |
| `group:memory` | `memory_search`, `memory_get` | 记忆检索 |
| `group:automation` | `cron`, `gateway` | 定时任务、网关管理 |

**执行流程**：模型输出结构化工具调用 → 运行时拦截 → 在沙箱/宿主执行 → 捕获结果 → 作为新消息注入对话 → 模型继续生成。

**工具策略五级级联**（从高到低）：
1. 全局允许/拒绝列表
2. Provider 级覆盖
3. Agent 级覆盖
4. 沙箱策略
5. 仅所有者限制

**拒绝列表永远优先。**

### 3.3 六种输入触发源

OpenClaw 不仅响应用户消息，还有五种**主动触发**方式：

```
① 聊天消息（12+ 平台） ← 被动
② 心跳事件（默认每30分钟）← 主动
③ Cron 定时任务         ← 主动
④ Hooks（钩子）         ← 事件驱动
⑤ Webhooks             ← 外部触发
⑥ Agent 间消息          ← 系统内部
```

**心跳系统采用两层策略**：先执行廉价的确定性脚本检查变化（新邮件？日历变更？告警？），仅在发现显著变化时才调用 LLM 分析决策。这大幅节省了 token 消耗。

---

## 第四部分：记忆系统 —— OpenClaw 的核心创新

这是 OpenClaw 与普通 AI 聊天最本质的区别。

### 4.1 三层记忆架构

```
┌─────────────────────────────────────────────┐
│          Layer 3: 会话记忆                    │
│  sessions/YYYY-MM-DD-<slug>.md              │
│  自动保存对话，带 LLM 生成的描述性 slug         │
│  可索引、可搜索                               │
├─────────────────────────────────────────────┤
│          Layer 2: 临时记忆（每日日志）          │
│  memory/YYYY-MM-DD.md                       │
│  追加式日志，启动时自动加载今天+昨天的记录       │
├─────────────────────────────────────────────┤
│          Layer 1: 持久记忆                    │
│  MEMORY.md                                  │
│  策划的长期知识：决策、约定、目标、关键事实       │
│  ⚠️ 仅在私信会话中加载，绝不在群组中暴露        │
└─────────────────────────────────────────────┘
```

### 4.2 向量索引与混合搜索

**存储后端**：SQLite + `sqlite-vec` 扩展

**分块策略**：
- 目标块大小：约 400 token（~1,600 字符）
- 块间重叠：80 token（~320 字符）防止边界上下文丢失
- 每个块有 SHA-256 哈希用于缓存

**嵌入自动选择**（优先级从高到低）：
1. 本地 GGUF 模型（`embeddinggemma-300m`，约 0.6GB，免费）
2. OpenAI `text-embedding-3-small`（1536 维）
3. Gemini `gemini-embedding-001`（768 维）
4. Voyage → Mistral → 禁用

**混合搜索算法**：

```
最终得分 = 0.7 × 向量余弦相似度 + 0.3 × BM25关键词得分
```

- **向量搜索**（权重 0.7）：捕获语义等价，如"gateway host"匹配"运行网关的机器"
- **BM25 搜索**（权重 0.3）：精确词汇匹配，擅长错误码、函数名、标识符

**后处理**：
- MMR 重排序（`lambda: 0.7`）：平衡相关性与多样性
- 时间衰减（`halfLife: 30天`）：近期记忆自然排名更高

### 4.3 上下文窗口管理：压缩前记忆刷写

**这是 OpenClaw 记忆系统最关键的创新。**

当对话接近上下文窗口限制时（约 176K / 200K token），系统触发一个**静默 Agent 轮次**：

```
长对话命中上下文限制
    │
    ▼
触发「静默」代理回合
    │
    ▼
系统告诉 AI: "你即将丢失上下文。现在将所有重要内容写入记忆文件。"
    │
    ▼
AI 将决策、状态变化、经验教训提取到 memory/YYYY-MM-DD.md
    │
    ▼
旧消息被压缩/截断
    │
    ▼
后续每轮 Auto-Recall 重新注入相关记忆
```

**关键设计**：记忆存储在上下文窗口**外部**，不受压缩影响。即使对话被截断，重要信息已经持久化，可通过语义搜索随时召回。

---

## 第五部分：多 Agent 编排 —— 从单体到集群

### 5.1 子 Agent 生成

通过 `sessions_spawn()` 创建隔离的子 Agent 会话：

```
主 Agent (Zoe)
   ├── spawn → 子 Agent A (Codex，写后端代码)
   ├── spawn → 子 Agent B (Claude Code，写前端)
   └── spawn → 子 Agent C (Gemini，设计 UI)
```

每个子 Agent 拥有：
- 独立的工作空间
- 独立的工具集（程序员有写权限，审查者仅读权限）
- 可使用不同 LLM 模型
- 独立的记忆/会话历史

### 5.2 Agent 间通信

`sessions_send` 支持 Agent 之间作为**对等体**直接通信（不仅是父子关系）：
- **发送即忘**（fire-and-forget）
- **同步等待响应**

可寻址会话键如 `pipeline:<project>:<role>` 实现精确路由。

### 5.3 Lobster 工作流引擎：确定性编排

OpenClaw 内置 Lobster 工作流引擎，核心理念：**不要用 LLM 做流程编排，LLM 只做创造性工作。**

```yaml
# dev-pipeline.lobster
steps:
  - code-review:
      programmer -> reviewer -> parse
      loop.condition: shell 命令评估是否通过
      maxIterations: 3    # 最多重试 3 次
  - testing:
      tester agent 运行测试
  - notification:
      Telegram 通知结果
```

流程控制保持在确定性代码中（YAML 工作流、循环条件、会话路由），创造性工作留给 AI Agent。

---

## 第六部分：安全模型 —— 多层防护

### 6.1 网络层

- **默认仅绑定 127.0.0.1**，防止公网暴露
- 远程访问必须通过 SSH 隧道或 Tailscale

### 6.2 认证层

- Token / 密码认证
- 设备配对（challenge-response 机制）
- 配对后发放 device token，作用域限定为 role + scopes

### 6.3 Docker 沙箱隔离

**核心原则**："Gateway 留在宿主机；工具执行在隔离沙箱中。"

| 沙箱模式 | 说明 |
|---------|------|
| `off`（默认） | 无沙箱 |
| `non-main` | 仅沙箱群组/channel 会话 |
| `all` | 沙箱所有会话 |

| 沙箱作用域 | 说明 |
|-----------|------|
| `session` | 每个会话独立容器（默认） |
| `agent` | 每个 Agent 一个容器 |
| `shared` | 所有会话共享一个容器 |

**被沙箱化的工具**：`exec`、`read`/`write`/`edit`、进程管理、浏览器自动化。

### 6.4 已知安全风险

- 沙箱**默认关闭**
- API 密钥明文存储
- 曾有 135,000+ 实例被暴露
- Meta AI 安全研究员报告 Agent 在收件箱"失控"删除 200 封邮件

---

## 第七部分：Elvis Sun 的"一人开发团队"架构

这是真实发生在 2026 年 1 月的案例。

### 7.1 核心数据

- **日均约 50 次 commit**，单日最高 94 次
- **30 分钟内完成 7 个 PR**
- 最疯狂的一天开了 3 个客户会议，**一次都没打开代码编辑器**
- 用于构建真实的 B2B SaaS 产品
- 成本：每月 $190（Claude $100 + Codex $90）

### 7.2 双层设计

```
┌──────────────────────────────────────────────┐
│           编排层 (Orchestration Layer)          │
│                                              │
│   OpenClaw + Zoe (编排器 Agent)               │
│                                              │
│   持有:                                       │
│   · 所有客户数据（Obsidian 知识库）              │
│   · 会议记录（自动同步）                        │
│   · 历史决策与成败记录                          │
│   · 生产数据库只读访问                          │
│   · 管理员 API 权限                            │
│                                              │
│   职责:                                       │
│   · 理解业务需求                               │
│   · 拆解任务                                   │
│   · 为每个 Agent 定制 Prompt（带业务上下文）      │
│   · 选择最佳模型                               │
│   · 监控进度                                   │
│   · 失败时分析原因并重写 Prompt                  │
│   · 通过 Telegram 通知                         │
└───────────┬────────────┬────────────┬────────┘
            │            │            │
    ┌───────▼──┐  ┌──────▼───┐  ┌────▼─────┐
    │  Codex   │  │ Claude   │  │ Gemini   │
    │  Agent   │  │ Code     │  │ Agent    │
    │          │  │ Agent    │  │          │
    │ 90%任务  │  │ 前端/Git │  │ UI设计   │
    │ 后端逻辑 │  │ 速度型   │  │ 审美型   │
    │ 复杂Bug  │  │          │  │          │
    └──────────┘  └──────────┘  └──────────┘
         执行层 (Execution Layer)

    · 只拿到"完成任务需要的最小上下文"
    · 永远不接触生产数据库
    · 永远看不到客户敏感信息
```

### 7.3 为什么需要双层？

**根本问题**：上下文窗口是固定的。

```
方案 A：把业务上下文塞给 Claude Code
→ 代码空间不够 → 写出的代码质量差

方案 B：把代码塞给 Claude Code
→ 没有业务上下文 → 不知道为谁写、为什么写

方案 C（Elvis 的方案）：分两层
→ 编排层持有业务上下文，翻译成精确 Prompt
→ 执行层专注代码，上下文全部留给代码
→ 两层各自发挥最大效能
```

### 7.4 完整工作流（8 步从需求到上线）

```
客户电话提需求
    │
    ▼
Step 1: Zoe 理解需求（零解释成本，会议记录已自动同步到 Obsidian）
    │    · 给客户充值（管理员 API）
    │    · 拉取客户配置（生产数据库只读）
    │    · 生成精确 Prompt 并启动 Agent
    ▼
Step 2: 创建隔离环境
    │    · git worktree（独立分支）
    │    · tmux 会话（后台运行，可中途干预）
    │    · 任务记录到 JSON 文件
    ▼
Step 3: 自动监控（Cron 每 10 分钟）
    │    · 检查客观事实：tmux 活着？PR 创建了？CI 状态？
    │    · 不问 Agent 进度（省 token）
    │    · 只在需要人工介入时才通知
    ▼
Step 4: Agent 创建 PR
    │    · 代码提交 → 推送 → gh pr create --fill
    │    · 此时不通知（PR ≠ 完成）
    ▼
Step 5: 三 AI 审查
    │    · Codex Reviewer：边界情况、逻辑错误、竞态条件（最靠谱）
    │    · Gemini Code Assist：安全问题、扩展性问题（免费好用）
    │    · Claude Code Reviewer：过度谨慎，非 critical 直接跳过
    ▼
Step 6: 自动化测试
    │    · Lint + TypeScript + 单元测试 + E2E + Playwright
    │    · UI 改动必须附截图，否则 CI 失败
    ▼
Step 7: 人工 Review（5-10 分钟）
    │    · CI 全绿 + 三个 AI 批准 + 截图展示
    │    · 很多 PR 只看截图就合并
    ▼
Step 8: 合并上线 ✅
         每天 Cron 清理孤立 worktree 和任务记录
```

### 7.5 改进版 Ralph Loop：动态学习

**传统 Ralph Loop**：拉取上下文 → 生成输出 → 评估结果 → 保存学习。每次循环 Prompt 相同。

**Elvis 的改进**：失败后，Zoe **分析失败原因并重写 Prompt**。

```
❌ 静态 Prompt（传统方式）:
   "实现自定义模板功能"

✅ 动态调整后的 Prompt（Elvis 方式）:
   "停。客户要的是 X，不是 Y。这是他们在会议里的原话：
   '我们希望保存现有配置，而不是从头创建新的。'
   重点做配置复用，不要做新建流程。"
```

Zoe 能做这种调整，因为她有执行层 Agent 没有的上下文：客户说了什么、公司做什么、上次为什么失败。

**成功模式会被记录**：
- "这种 Prompt 结构对账单功能很有效"
- "Codex 需要提前拿到类型定义"
- "总是要包含测试文件路径"

**奖励信号**：CI 通过 + 三个 code review 通过 + 人工合并。任何失败都触发循环。时间越长，Prompt 越精准。

### 7.6 Zoe 的主动工作模式

```
早上: 扫描 Sentry → 发现 4 个新错误 → 启动 4 个 Agent 调查修复
会议后: 扫描会议记录 → 发现 3 个功能需求 → 启动 3 个 Codex
晚上: 扫描 git log → 启动 Claude Code 更新 changelog 和文档

Elvis 散步回来，Telegram 显示：
"7 个 PR 准备好了。3 个新功能，4 个 bug 修复。"
```

### 7.7 Agent 选择策略

| 任务类型 | 分配给 | 原因 |
|---------|--------|------|
| 后端逻辑、复杂 Bug、多文件重构 | **Codex (gpt-5.3-codex)** | 慢但彻底，占 90% 任务 |
| 前端工作、Git 操作 | **Claude Code (claude-opus-4.5)** | 快，权限问题少 |
| UI 设计 | **Gemini** | 有设计审美，先生成 HTML/CSS 规范 |
| 架构决策 | **Claude Opus** | 深度推理 |
| 心跳检测、简单查询 | **Gemini Flash-Lite** | $0.50/百万 token，极低成本 |

**成本优化效果**：合理分层可节省 65%+ 的 API 成本。

### 7.8 硬件瓶颈

意外的限制不是 token 成本，而是 **RAM**。

每个 Agent 需要：独立 worktree + 独立 node_modules + 构建/类型检查/测试运行。5 个 Agent 同时跑 = 5 个并行 TypeScript 编译器 + 5 个测试运行器 + 5 套依赖。

- Mac Mini 16GB：最多 4-5 个 Agent，再多开始 swap
- Mac Studio M4 Max 128GB：Elvis 的升级目标（$3,500）

---

## 第八部分：其他真实生产案例

### 案例 1：Nat Eliason 的 Felix Bot

给 OpenClaw Bot $1,000 启动资金，**3 周产生 $14,718 收入**，目前每周 $4,000。

**三层记忆系统**：
1. **知识图谱**（Layer 1）：使用 PARA 方法论，存储关于人和项目的持久性事实
2. **每日笔记**（Layer 2）：每天一个 Markdown 文件记录活动，夜间自动提取到 Layer 1
3. **隐性知识**（Layer 3）：编码个人细节——沟通偏好、工作流习惯、硬性规则

### 案例 2：6-Agent 内容生产团队

| Agent | 功能 | 调度 |
|-------|------|------|
| 研究员 | 每 2 小时扫描趋势 | 5:00 AM |
| 写手 | 创建内容大纲 | 8:00 AM |
| 设计师 | 生成幻灯片 | 8:30 AM |
| 审查员 | 质量检查 | 8:45 AM |
| 组装员 | ffmpeg 创建视频 | 9:00 AM |
| 协调员 | 最终审批 | 9:15 AM |

运营成本：每天约 $2。

### 案例 3：25 分钟交付 SaaS Landing Page

Lead Agent 分解任务 → Coding Agent 编写代码 → Review Agent 验证质量 → Deploy Agent 部署上线。25 分钟完成，传统自由职业者需要 $500-2000 和 1-2 周。

---

## 第九部分：插件与生态

### 插件四种类型

| 类型 | 说明 | 示例 |
|------|------|------|
| Channels | 消息平台集成 | Matrix、Zalo、MS Teams |
| Tools | Agent 能力扩展 | 浏览器自动化、数据库操作 |
| Providers | AI 模型推理 | 自定义 LLM 端点 |
| Memory | 搜索后端 | QMD 向量搜索 |

### MCP（Model Context Protocol）集成

OpenClaw 原生支持 MCP 服务器（JSON-RPC 2.0 over stdio/HTTP）：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "ghp_xxx" }
    }
  }
}
```

社区已构建超过 **1,000 个 MCP 服务器**，覆盖 Google Drive、Slack、数据库等。每个 Agent 可拥有独立的 MCP 服务器集合。

### Skills 系统

模块化的 `SKILL.md` 文件，带 YAML frontmatter + 自然语言指令。添加即激活，不需重启。ClawHub 技能注册中心已有 **5,700+ 社区技能**。

### Mission Control 团队编排

Mission Control 是 OpenClaw 的集中运营和治理平台：
- **对话式 Squad 设计**：描述团队需求，自动生成 Agent 规格
- **一键部署**：自动创建会话、安装技能、配置心跳 Cron
- **看板式任务管理**：Backlog → In Progress → In Review → Done
- **心跳监控**：Agent 每 2-5 分钟签到，接收任务分配和通知

---

## 第十部分：与竞品对比

| 维度 | OpenClaw | Devin AI | Claude Code | n8n |
|------|---------|---------|-------------|-----|
| **定位** | 消息优先通用自动化 | 端到端自治软件工程 | 终端编码助手 | 确定性工作流 |
| **价格** | 免费+API 成本 | $500+/月 | $0-20/月 | 免费/$20 起 |
| **通道** | 50+ 消息平台 | Web IDE | 终端/IDE | Webhook/API |
| **记忆** | 跨会话持久化 | 项目级 | 会话级 | 工作流变量 |
| **主动性** | 心跳+Cron 主动工作 | 被动等待指令 | 被动等待指令 | 触发器驱动 |
| **安全** | 最弱（无默认沙盒） | 云端沙盒 | 本地执行 | 确定性执行 |

### 快速决策矩阵

| 你的需求 | 最佳选择 |
|---------|---------|
| 编码自动化 | Claude Code / Devin AI |
| 一人开发团队 | OpenClaw + Claude Code + Codex |
| 业务工作流 | n8n |
| 最大定制化 | LangChain / CrewAI |
| 非技术用户 | Manus AI / Zapier |

---

## 核心要点总结

1. **三层架构**：Channel 层屏蔽平台差异 → Gateway 层编排管理 → Provider 层对接模型
2. **六阶段消息流水线**：从消息摄入到响应投递，完全自动化
3. **三层记忆 + 混合搜索**：临时/持久/会话记忆，向量+BM25 混合检索，压缩前刷写保证不丢失
4. **Agent 运行四阶段**：上下文组装 → 模型推理 → 工具执行 → 状态持久化
5. **Lobster 确定性编排**：流程控制用 YAML 状态机，创造性工作留给 LLM
6. **双层分工**（Elvis 模式）：编排层持有业务上下文，执行层专注代码
7. **动态学习**：失败后分析原因重写 Prompt，成功模式持久记录，系统越用越聪明

---

## 参考资料

- [OpenClaw 官方文档](https://docs.openclaw.ai/)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Architecture Deep Dive - DeepWiki](https://deepwiki.com/openclaw/openclaw/15.1-architecture-deep-dive)
- [OpenClaw Architecture Overview - Substack](https://ppaolo.substack.com/p/openclaw-system-architecture-overview)
- [Gateway Control Plane](https://openclawcn.com/en/docs/deep-dive/framework-focus/gateway-control-plane/)
- [Memory System Deep Dive](https://snowan.gitbook.io/study-notes/ai-blogs/openclaw-memory-system-deep-dive)
- [Ralph Loop vs OpenClaw](https://kenhuangus.substack.com/p/ralph-vs-openclaw-understanding-process)
- [Deterministic Multi-Agent Pipeline](https://dev.to/ggondim/how-i-built-a-deterministic-multi-agent-dev-pipeline-inside-openclaw-and-contributed-a-missing-4ool)
- [Elvis Sun on X](https://x.com/elvissun/status/2025920521871716562)
- [Nat Eliason: Build a Business That Runs Itself](https://creatoreconomy.so/p/use-openclaw-to-build-a-business-that-runs-itself-nat-eliason)
- [AI Dev Team - LobsterLair](https://lobsterlair.xyz/blog/ai-dev-team-openclaw)
- [OpenClaw Security - Microsoft Blog](https://www.microsoft.com/en-us/security/blog/2026/02/19/running-openclaw-safely-identity-isolation-runtime-risk/)
- [Multi-Agent Code Review - Clawctl](https://www.clawctl.com/blog/multi-agent-code-review)
- [Mission Control](https://github.com/abhi1693/openclaw-mission-control)
- [中文汉化版 OpenClaw](https://github.com/1186258278/OpenClawChineseTranslation)
- [中文版 OpenClaw（含飞书支持）](https://github.com/jiulingyun/openclaw-cn)
- [保姆级安装教程（腾讯云）](https://cloud.tencent.com/developer/article/2626160)
