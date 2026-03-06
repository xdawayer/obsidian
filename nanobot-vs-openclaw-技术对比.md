# Nanobot vs OpenClaw 技术框架对比分析

## 一、项目定位

| 维度 | Nanobot (HKUDS) | OpenClaw |
|------|-----------------|----------|
| **定位** | 超轻量级个人 AI 助手框架 | 全功能个人 AI 助手平台 |
| **核心理念** | "99% fewer lines of code"，面向研究和快速定制 | 全平台覆盖、企业级扩展性 |
| **代码规模** | ~11K 行 Python（核心 agent ~4K 行） | 数万行 TypeScript + Swift/Kotlin 原生应用 |
| **目标用户** | 研究者、极客、需要快速原型的开发者 | 产品化用户、需要多端体验的个人/团队 |

---

## 二、技术架构对比

### 2.1 整体架构

**Nanobot — 单进程消息总线架构**
```
Channel Layer (12个渠道) → Message Bus (异步队列) → Agent Loop → Tool Execution
                                                      ↕
                                              Session / Memory / Skills
```
- 单一 Python 进程运行所有组件
- 消息通过异步队列路由
- Agent Loop 是核心主循环，串行处理消息

**OpenClaw — Gateway + 多客户端 WebSocket 架构**
```
Gateway (WebSocket Server) ←→ CLI / macOS App / iOS App / Android App / Web UI
         ↕
Channel Integrations + Agent Executor (ACP 隔离进程) + Plugin System
```
- Gateway 作为长驻守护进程，暴露 RPC API
- 多个客户端通过 WebSocket 连接
- Agent 通过 ACP (Agent Control Protocol) 在隔离进程中执行
- 插件通过 jiti 动态加载

### 2.2 核心差异

| 架构特性 | Nanobot | OpenClaw |
|---------|---------|----------|
| **进程模型** | 单进程，子任务用 asyncio | 多进程，ACP 隔离 agent |
| **通信协议** | 内部异步队列 | WebSocket RPC (类型安全) |
| **客户端** | CLI + 消息渠道 | CLI + Web UI + macOS/iOS/Android 原生应用 |
| **状态管理** | JSONL 文件 + Markdown | 文件 + 可选向量数据库 (LanceDB) |
| **隔离性** | 共享进程空间 | Agent 进程级隔离 |

---

## 三、技术栈对比

| 维度 | Nanobot | OpenClaw |
|------|---------|----------|
| **主语言** | Python 3.11+ | TypeScript (Node 22+) |
| **辅助语言** | TypeScript (WhatsApp Bridge) | Swift (macOS/iOS), Kotlin (Android) |
| **包管理** | uv / pip | pnpm (monorepo workspace) |
| **配置验证** | Pydantic | TypeBox |
| **CLI 框架** | Typer + Rich | Commander.js + @clack/prompts |
| **LLM 路由** | LiteLLM (统一接口) | 各 SDK 直连 (Anthropic/OpenAI/Google SDK) |
| **测试框架** | Pytest + pytest-asyncio | Vitest (覆盖率要求 70%) |
| **构建工具** | pyproject.toml (uv) | tsdown + Vite |
| **容器基础镜像** | uv:python3.12-bookworm-slim | Node 22-bookworm |

### LLM 集成方式差异

**Nanobot**: 重度依赖 **LiteLLM** 作为统一中间层
- 优势：一个接口适配 20+ provider，代码极简
- 劣势：受 LiteLLM 版本/bug 影响，调试链路长

**OpenClaw**: 直接集成各家官方 SDK
- 优势：对每个 provider 有更精细的控制（如 Anthropic 缓存 TTL、Google 参数保留）
- 劣势：每增加一个 provider 需要写适配代码，维护成本高

---

## 四、消息渠道对比

| 渠道 | Nanobot | OpenClaw |
|------|---------|----------|
| Telegram | python-telegram-bot | grammY |
| Discord | 自实现 WebSocket | discord.js |
| WhatsApp | Node.js Bridge (Baileys) | Baileys + Playwright |
| Slack | slack-sdk | @slack/bolt |
| Signal | - | signal-cli 封装 |
| iMessage | - | 原生支持 |
| Matrix | matrix-nio | 插件 (extensions/) |
| 飞书 (Feishu) | lark-oapi (WebSocket) | - |
| 钉钉 (DingTalk) | dingtalk-stream | - |
| QQ | qq-botpy | - |
| Email | IMAP + SMTP | - |
| LINE | - | 内置支持 |
| Teams | - | 插件 (extensions/) |
| Zalo | - | 插件 (extensions/) |
| IRC | - | 插件 (extensions/) |
| **合计** | ~12 渠道 | ~15+ 渠道 (含插件) |

**关键差异**：
- Nanobot 对中国市场渠道支持更好（飞书、钉钉、QQ）
- OpenClaw 对西方市场渠道更全（Signal、iMessage、Teams、LINE）
- OpenClaw 的渠道可通过插件机制无限扩展

---

## 五、Agent 能力对比

### 5.1 工具系统

| 特性 | Nanobot | OpenClaw |
|------|---------|----------|
| **内置工具数** | ~10 个 | 更多（含浏览器自动化等） |
| **文件操作** | read/write/edit/list_dir | read/write + 安全策略 |
| **Shell 执行** | exec (带黑名单) | bash (带审批流程 + 沙箱) |
| **网页搜索** | Brave Search API | 可配置 |
| **网页抓取** | readability-lxml | Playwright 浏览器 |
| **浏览器自动化** | 无 | Playwright 完整支持 |
| **定时任务** | cron_add/list/remove | 通过插件/hook |
| **子 Agent** | spawn_task (后台) | ACP 隔离进程 (更安全) |
| **MCP 支持** | 原生 (stdio + HTTP) | mcporter 桥接 |
| **工具审批** | 无 (信任模型) | 危险操作需用户确认 |

### 5.2 记忆系统

| 特性 | Nanobot | OpenClaw |
|------|---------|----------|
| **短期记忆** | Session 消息历史 (JSONL) | Session 文件存储 |
| **长期记忆** | MEMORY.md (Markdown) | 可选 LanceDB 向量数据库 |
| **审计日志** | HISTORY.md (可搜索) | 通过日志系统 |
| **记忆整合** | LLM 驱动的自动 consolidation | 插件可选 |
| **语义搜索** | 无（纯文本） | LanceDB 向量搜索（可选） |

**关键差异**：Nanobot 的记忆系统简洁透明（纯 Markdown 文件，人类可直接阅读编辑）；OpenClaw 支持向量数据库做语义搜索，适合大规模知识管理。

### 5.3 技能系统

| 特性 | Nanobot | OpenClaw |
|------|---------|----------|
| **技能数量** | 9 个内置 | 54+ 个内置 |
| **技能格式** | SKILL.md (Markdown + YAML frontmatter) | 目录 + Markdown |
| **依赖检查** | 自动检测 (bins/env) | 手动配置 |
| **社区分享** | ClawHub 市场 | ClawHub 市场 |
| **动态加载** | 支持 (按需/常驻) | 支持 |

---

## 六、扩展性对比

### Nanobot 扩展方式

1. **新增 Provider**: 在 `registry.py` 添加 ProviderSpec（约 10 行代码）
2. **新增渠道**: 继承 BaseChannel，实现 receive/send（~100 行代码）
3. **新增工具**: 继承 Tool 基类，注册到 registry（~50 行代码）
4. **新增技能**: 创建 SKILL.md 文件即可（无代码）
5. **MCP 集成**: 配置 JSON 即可

**扩展成本**：极低，几乎每种扩展都可在 10-100 行内完成。

### OpenClaw 扩展方式

1. **新增 Provider**: 编写 SDK 适配器 + Auth Profile
2. **新增渠道**: 编写 extension 插件包（含 TypeScript + package.json）
3. **新增工具**: 在插件中定义 JSON Schema + 执行函数
4. **新增技能**: 目录 + Markdown 文件
5. **MCP 集成**: 通过 mcporter 桥接
6. **HTTP 路由**: 插件可注册自定义 API 端点
7. **Hook**: 订阅生命周期事件
8. **原生应用**: Swift/Kotlin 开发

**扩展能力**：远超 Nanobot，但复杂度也更高。

---

## 七、部署对比

| 维度 | Nanobot | OpenClaw |
|------|---------|----------|
| **最简部署** | `pip install nanobot && nanobot gateway` | `npx openclaw gateway` |
| **Docker** | 单容器 (~1GB 限制) | 多容器 (gateway + sandbox) |
| **系统服务** | systemd 集成 | systemd / launchd |
| **云部署** | Docker Compose | Docker + Render.com + Fly.io |
| **资源占用** | ~256MB RAM | 更高 (Node.js + 可选 Playwright) |
| **原生应用** | 无 | macOS/iOS/Android |

---

## 八、安全模型对比

| 安全特性 | Nanobot | OpenClaw |
|---------|---------|----------|
| **文件系统** | 路径遍历保护 + workspace 限制 | 白名单机制 |
| **Shell 执行** | 命令黑名单 (rm -rf / 等) | 审批工作流 + Docker 沙箱 |
| **Agent 隔离** | 共享进程 (无隔离) | ACP 进程隔离 |
| **认证** | 渠道 allowFrom 白名单 | Gateway Token + 设备配对 |
| **密钥管理** | config.json (0600 权限) | 专用 credentials 目录 |
| **MCP 安全** | 内置处理 | mcporter 桥接隔离 |

**关键差异**：OpenClaw 的安全模型更成熟（进程隔离、审批工作流、设备配对），适合更严格的生产环境。Nanobot 采用简单信任模型，适合个人使用或受信环境。

---

## 九、测试对比

| 维度 | Nanobot | OpenClaw |
|------|---------|----------|
| **测试框架** | Pytest | Vitest |
| **测试文件** | 16+ | 大量 (多配置文件) |
| **覆盖率要求** | 无明确要求 | 70% (lines/branches/functions) |
| **测试类型** | 单元测试为主 | 单元 + 集成 + E2E + Live |
| **CI/CD** | 未明确 | Pre-commit hooks + 多环境测试 |

---

## 十、综合优劣分析

### Nanobot 优势

1. **极简架构**：4K 行核心代码，容易理解和修改，适合学术研究
2. **上手快**：pip install 即可运行，配置简单
3. **中国市场友好**：原生支持飞书、钉钉、QQ、微信（通过 WhatsApp Bridge 思路）
4. **LiteLLM 统一接口**：一行配置切换 20+ LLM provider
5. **Prompt 缓存**：Anthropic prompt caching 降低成本
6. **记忆透明**：MEMORY.md + HISTORY.md 人类可读可编辑
7. **研究友好**：代码干净、模块清晰、易于实验
8. **资源占用低**：256MB RAM 即可运行

### Nanobot 劣势

1. **无原生客户端**：仅 CLI + 消息渠道，无 GUI
2. **安全模型简单**：无进程隔离、无审批工作流
3. **无向量搜索**：记忆系统为纯文本，无语义检索
4. **单进程瓶颈**：高并发场景受限
5. **浏览器自动化缺失**：无 Playwright 等高级工具
6. **插件生态较小**：9 个内置技能 vs OpenClaw 54+
7. **测试覆盖不足**：无明确覆盖率要求

### OpenClaw 优势

1. **全平台覆盖**：CLI + Web + macOS + iOS + Android
2. **企业级安全**：进程隔离、审批流程、设备配对、Docker 沙箱
3. **丰富的生态**：54+ 技能、42+ 扩展插件
4. **向量记忆**：LanceDB 支持语义搜索
5. **浏览器自动化**：Playwright 集成
6. **精细 Provider 控制**：直连各家 SDK，可用缓存 TTL 等高级特性
7. **严格测试**：70% 覆盖率要求，多种测试类型
8. **插件架构成熟**：支持工具、渠道、Hook、HTTP 路由、后台服务等多种扩展

### OpenClaw 劣势

1. **复杂度高**：代码量大，学习曲线陡峭
2. **资源消耗大**：Node.js + 可选 Playwright/Docker，内存占用更高
3. **缺少中国渠道**：无飞书、钉钉、QQ 原生支持
4. **维护成本高**：每个 Provider 需要单独适配器
5. **TypeScript 生态依赖**：对非 TS 开发者不友好
6. **Monorepo 复杂**：pnpm workspace + 多包管理增加构建复杂度

---

## 十一、选型建议

| 场景 | 推荐方案 | 原因 |
|------|---------|------|
| 学术研究 / Agent 实验 | **Nanobot** | 代码量少，架构清晰，易于修改和发论文 |
| 中国市场部署 | **Nanobot** | 飞书/钉钉/QQ 原生支持 |
| 个人轻量助手 | **Nanobot** | 资源占用低，配置简单 |
| 多端产品化需求 | **OpenClaw** | 原生 App + Web UI + 丰富插件 |
| 企业级安全要求 | **OpenClaw** | 进程隔离、审批流程、沙箱 |
| 大规模知识管理 | **OpenClaw** | 向量数据库 + 语义搜索 |
| 高级浏览器交互 | **OpenClaw** | Playwright 集成 |
| 快速原型验证 | **Nanobot** | 上手快，扩展成本低 |

---

## 十二、总结

**Nanobot** 和 **OpenClaw** 代表了 AI 助手框架设计的两种哲学：

- **Nanobot = Unix 哲学**：Do one thing well. 极简、透明、可组合。用最少的代码实现核心 Agent 功能，把复杂性留给用户按需扩展。适合研究者和极客。

- **OpenClaw = 平台哲学**：Full-featured platform. 全面、安全、产品化。提供完整的客户端矩阵、丰富的插件生态、企业级安全模型。适合需要开箱即用的产品化场景。

两者在技术实现上有明显的互补关系——Nanobot 对中国市场渠道的支持和 OpenClaw 对西方市场的覆盖，恰好形成了地理互补。
