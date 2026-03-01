---
title: "OpenClaw 视频攻略 — 赋范课堂28集全解"
date: 2026-03-01
tags:
  - AI
  - OpenClaw
  - Agent
  - 视频攻略
  - 赋范课堂
  - HR数字员工
aliases:
  - OpenClaw视频教程
  - 赋范课堂OpenClaw
  - OpenClaw 28集攻略
description: "赋范课堂28集 OpenClaw 视频系列的完整学习笔记与攻略，涵盖从部署到原理精讲到实战 AI HR 数字员工开发，总时长约5.4小时"
---

# OpenClaw 视频攻略 — 赋范课堂28集全解

> [!abstract] 系列概览
> **UP主**：赋范课堂
> **平台**：B站（BV115AbzjENY）
> **集数**：28集 | **总时长**：约5.4小时（324分钟）
> **主题**：OpenClaw 从零部署 → 架构原理精讲 → Mini OpenClaw 实现 → AI HR 数字员工实战
> **适合人群**：对 AI Agent 感兴趣的开发者、想搭建企业级智能体的技术人员
> **B站链接**：`https://www.bilibili.com/video/BV115AbzjENY`

---

## 四大模块总览

```
┌─────────────────────────────────────────────────────────────┐
│                    赋范课堂 OpenClaw 28集                      │
├───────────┬───────────┬────────────┬────────────────────────┤
│ 模块一     │ 模块二     │ 模块三      │ 模块四                  │
│ 入门与背景  │ 部署与规划  │ 架构与实现   │ AI HR 实战              │
│ P1-P4     │ P5-P10    │ P11-P18    │ P19-P28               │
│ ~21分钟    │ ~75分钟    │ ~108分钟    │ ~119分钟               │
│           │           │            │                        │
│ 项目介绍   │ 本地部署   │ 原理精讲     │ 基础架构回顾             │
│ 开源历程   │ 三系统部署  │ 记忆系统     │ 内置工具                │
│ 核心功能   │ 远程连接   │ Skills系统  │ 插件与Skills            │
│ 行业趋势   │ Mini规划   │ 代码详解     │ 人格与记忆              │
│           │ 记忆策略   │ 需求文档     │ HR开发实战(上下)          │
│           │ Skills策略 │ README     │ 重置+音频+测试           │
└───────────┴───────────┴────────────┴────────────────────────┘
```

---

## 模块一：入门与背景（P1-P4，约21分钟）

> [!info] 模块概要
> 本模块介绍 OpenClaw 项目的背景、发展历程、核心功能以及行业趋势分析。适合完全不了解 OpenClaw 的新手快速建立认知框架。

### 分集详解表

| 集数 | 标题 | 时长 | 核心要点 |
|------|------|------|----------|
| P1 | 一口气快速入门OpenClaw从部署到原理精讲到实战AI HR数字员工 | ~1分钟 | 系列总览与导言 |
| P2 | OpenClaw项目开源与发展历程 | ~7.7分钟 | 项目开源背景与发展历史 |
| P3 | OpenClaw核心功能与用户反馈 | ~5.3分钟 | 核心功能特性、社区反馈 |
| P4 | OpenClaw爆火背后的时代契机：从AutoGPT到贾维斯时刻 | ~7.4分钟 | 行业趋势、AI Agent发展脉络 |

---

### P1：导言/总览（~1分钟）

**核心内容**：整个28集系列的路线图概述。

- 系列分为三大阶段：部署入门 → 原理精讲 → 实战开发
- 最终目标：从零开发一个企业可用的 AI HR 数字员工
- 强调"从部署到原理到实战"的完整学习闭环

> [!tip] 学习建议
> 这一集虽短，但建议认真看完，帮助你建立整体学习路线的认知，明确每个阶段的目标。

---

### P2：OpenClaw项目开源与发展历程（~7.7分钟）

**核心内容**：OpenClaw 的诞生背景与开源历程。

- **项目起源**：由 Peter Steinberger 开发，最初名为 Clawdbot / Moltbot
- **开源协议**：MIT 许可证，完全免费
- **技术栈**：TypeScript（Node.js）编写
- **爆发节点**：2026年1月爆火，GitHub 迅速突破 10 万星
- **项目动态**：2026年2月14日，Steinberger 宣布加入 OpenAI，项目将移交至开源基金会
- **社区生态**：ClawHub 技能注册中心已有 5,700+ 社区技能

**关键理解**：OpenClaw 不是聊天机器人，而是一个**本地运行的 AI Agent 编排运行时**——能调度多个 AI 模型、执行真实操作、拥有持久记忆。

> 相关参考：[[docs/OpenClaw 完整技术架构与应用详解.md|完整技术架构]] 第一部分

---

### P3：OpenClaw核心功能与用户反馈（~5.3分钟）

**核心内容**：OpenClaw 的核心能力与社区真实反馈。

- **50+ 消息平台支持**：WhatsApp、Telegram、Slack、Discord、飞书、iMessage 等
- **持久记忆系统**：三层记忆架构（持久/临时/会话），跨会话不丢失
- **工具执行能力**：八大工具组，涵盖 Shell 执行、文件操作、网络搜索、浏览器自动化等
- **主动工作模式**：心跳系统 + Cron 定时任务，不需要人类主动触发
- **多模型调度**：可同时使用 Claude、GPT、Gemini、DeepSeek 等模型
- **Skills 即插即用**：Markdown 格式的技能文件，放入目录即生效

**用户反馈亮点**：
- Elvis Sun 案例：日均 50 次 commit，月成本仅 $190
- Nat Eliason 的 Felix Bot：3 周产生 $14,718 收入
- 25 分钟交付 SaaS Landing Page

> [!warning] 安全提醒
> 社区反馈中也暴露了安全隐患：沙箱默认关闭、曾有 13.5 万实例暴露到公网。部署时务必注意安全配置。

---

### P4：OpenClaw爆火背后的时代契机（~7.4分钟）

**核心内容**：行业大背景分析——从 AutoGPT 到"贾维斯时刻"。

- **AI Agent 发展脉络**：
  - 2023年：AutoGPT 引爆 Agent 概念，但实用性不足
  - 2024年：LangChain/CrewAI 等框架涌现，基础设施逐步成熟
  - 2025年：Claude Code、Cursor 等编码 Agent 验证了 Agent 的实用价值
  - 2026年：OpenClaw 实现了"通用 AI Agent"的突破——不仅编码，而是全能管家
- **为什么是"贾维斯时刻"**：OpenClaw 实现了钢铁侠 Jarvis 的核心特征——本地运行、持久记忆、主动工作、多能力协调
- **关键技术催化剂**：200K+ 上下文窗口、Function Calling 标准化、MCP 协议统一工具接入

> [!tip] 理解要点
> 本集帮助理解 OpenClaw 为什么在这个时间点爆火——不是偶然，而是 LLM 能力、协议标准化、社区需求三者交汇的结果。

---

## 模块二：部署与开发规划（P5-P10，约75分钟）

> [!info] 模块概要
> 本模块涵盖 OpenClaw 的本地部署、三大操作系统适配、远程连接配置，以及 Mini OpenClaw 的技术栈规划和核心功能实现策略。这是动手实践的起点。

### 分集详解表

| 集数 | 标题 | 时长 | 核心要点 |
|------|------|------|----------|
| P5 | OpenClaw零门槛本地部署指南 | ~9.5分钟 | 本地部署的基础步骤 |
| P6 | 三大操作系统OpenClaw零门槛部署流程 | ~10.1分钟 | Win/Mac/Linux 差异化部署 |
| P7 | OpenClaw远程连接方法 | ~12分钟 | SSH 隧道、Tailscale 等远程方案 |
| P8 | 适配国内环境的mini OpenClaw开发思路与核心技术栈规划 | ~18.3分钟 | Mini OpenClaw 技术栈规划 |
| P9 | OpenClaw无限对话记忆功能实现策略 | ~14.9分钟 | 记忆系统设计策略 |
| P10 | OpenClaw自由组装Skills功能实现策略 | ~9.7分钟 | Skills 模块化设计策略 |

---

### P5：零门槛本地部署指南（~9.5分钟）

**核心内容**：OpenClaw 本地部署的基础步骤。

**前置条件**：
- Node.js 22+
- 至少一个 AI 模型 API Key（OpenAI / Anthropic / Google / DeepSeek）

**部署三步走**：

```bash
# 第1步：全局安装
npm install -g openclaw@latest

# 第2步：运行引导向导（配置 API Key、选模型、安装守护进程）
openclaw onboard --install-daemon

# 第3步：开始对话
openclaw chat
```

**配置文件位置**：`~/.openclaw/openclaw.json`

**目录结构概览**：

```
~/.openclaw/
├── openclaw.json          ← 主配置文件
├── MEMORY.md              ← 持久记忆
├── memory/                ← 每日记忆（YYYY-MM-DD.md）
├── sessions/              ← 对话记录（JSONL 格式）
├── agents/                ← Agent 数据
├── skills/                ← 技能目录
└── workspace/             ← 工作区（AGENTS.md / SOUL.md / USER.md）
```

> [!tip] 国内部署提示
> 国内网络环境下，npm 安装可能需要配置镜像源。API Key 方面，DeepSeek 是国内可直接使用的选择。

---

### P6：三大操作系统部署流程（~10.1分钟）

**核心内容**：Windows / macOS / Linux 三个平台的部署差异。

**平台差异对照**：

| 平台 | Node.js 安装 | 守护进程方式 | 注意事项 |
|------|-------------|-------------|---------|
| **macOS** | Homebrew / nvm | launchd | 最推荐，开发体验最好 |
| **Windows** | 官网安装包 / nvm-windows | Windows Service | 需注意路径分隔符 |
| **Linux** | nvm / apt | systemd | 服务器部署首选 |

**macOS 示例**：

```bash
# Homebrew 安装 Node.js
brew install node@22

# 安装 OpenClaw
npm install -g openclaw@latest

# 引导安装（含 launchd 守护进程）
openclaw onboard --install-daemon
```

**关键配置项**：

```jsonc
{
  "models": {
    "default": "anthropic/claude-sonnet-4-20250514"
  },
  "agents": {
    "defaults": {
      "name": "Hal",
      "model": "anthropic/claude-sonnet-4-20250514"
    }
  }
}
```

> 交叉参考：→ P5 的基础部署 → P7 的远程连接

---

### P7：远程连接方法（~12分钟）

**核心内容**：如何从外部访问本地运行的 OpenClaw。

**安全第一原则**：OpenClaw Gateway 默认绑定 `127.0.0.1:18789`，仅本机可访问。

**三种远程方案**：

| 方案 | 安全性 | 复杂度 | 适用场景 |
|------|--------|--------|---------|
| **SSH 隧道** | 高 | 中 | 开发者日常使用 |
| **Tailscale** | 高 | 低 | 多设备组网 |
| **Cloudflare Tunnel** | 高 | 中 | 需要域名访问 |

**SSH 隧道示例**：

```bash
# 从远程机器建立 SSH 隧道
ssh -L 18789:127.0.0.1:18789 user@your-server

# 本地即可通过 localhost:18789 访问远程 OpenClaw Gateway
```

**WebSocket 协议要点**：
- 所有通信使用 JSON 文本帧
- 第一帧必须是 `connect` 握手请求
- 三种帧类型：Request（请求）、Response（响应）、Event（事件）

```
帧格式：
Request:  {type:"req", id, method, params}     客户端→Gateway
Response: {type:"res", id, ok, payload}         Gateway→客户端
Event:    {type:"event", event, payload, seq}   Gateway→客户端（推送）
```

> [!warning] 安全警告
> 永远不要将 18789 端口直接暴露到公网！曾有 135,000+ OpenClaw 实例因此被暴露。务必使用隧道方案。

---

### P8：Mini OpenClaw 技术栈规划（~18.3分钟）

**核心内容**：针对国内环境，从零规划一个精简版 Mini OpenClaw 的技术栈。

这是系列中非常关键的一集，时长较长，内容密度高。

**为什么要做 Mini 版**：
- 原版 OpenClaw 代码量大，不适合学习理解原理
- 国内环境需要适配（DeepSeek 等国内模型、网络环境）
- 抓住核心功能，去掉不必要的复杂性

**核心技术栈**：

```
┌─────────────────────────────────────────────┐
│           Mini OpenClaw 技术栈                │
├──────────────┬──────────────────────────────┤
│ LLM 调度     │ LangChain（统一模型接口）       │
│ 对话管理     │ LangChain Memory + 自定义持久化  │
│ 工具系统     │ LangChain Tools + Function Calling │
│ 向量存储     │ SQLite + sqlite-vec（轻量级）    │
│ 后端框架     │ FastAPI / Express              │
│ 前端（可选）  │ React / 命令行                  │
│ 国内模型     │ DeepSeek / 通义千问 / 智谱        │
└──────────────┴──────────────────────────────┘
```

**对标 OpenClaw 三层架构的简化映射**：

```
OpenClaw 三层              Mini OpenClaw 简化
┌──────────────┐          ┌──────────────┐
│ Channel 层   │    →     │ CLI / Web UI  │  (先做最简单的)
├──────────────┤          ├──────────────┤
│ Gateway 层   │    →     │ 单进程服务     │  (去掉分布式复杂性)
├──────────────┤          ├──────────────┤
│ Provider 层  │    →     │ LangChain     │  (统一模型接口)
└──────────────┘          └──────────────┘
```

> [!tip] 学习价值
> 这集的真正价值不在于 Mini OpenClaw 本身，而在于通过"做减法"的思路，帮你理解 OpenClaw 每个组件的必要性和核心职责。

> 交叉参考：→ P11 架构原理精讲 → P13 工业级记忆系统搭建

---

### P9：无限对话记忆功能实现策略（~14.9分钟）

**核心内容**：OpenClaw 记忆系统的设计原理与实现策略。

**三层记忆架构**：

```
┌─────────────────────────────────────────────┐
│    Layer 3: 会话记忆                          │
│    sessions/YYYY-MM-DD-<slug>.md            │
│    → 自动保存每次对话，带 LLM 生成的描述性 slug  │
├─────────────────────────────────────────────┤
│    Layer 2: 临时记忆（每日日志）                │
│    memory/YYYY-MM-DD.md                     │
│    → 追加式日志，启动时加载今天+昨天的记录       │
├─────────────────────────────────────────────┤
│    Layer 1: 持久记忆                          │
│    MEMORY.md                                │
│    → 长期知识：决策、约定、目标、关键事实         │
│    → 仅在私信会话中加载，群组中不暴露            │
└─────────────────────────────────────────────┘
```

**"无限"记忆的关键——压缩前记忆刷写**：

```
长对话接近上下文限制（~80% 的 200K token）
    │
    ▼
触发「静默」Agent 回合
    │
    ▼
系统提示 AI："你即将丢失上下文，现在将重要内容写入记忆文件"
    │
    ▼
AI 提取关键信息 → 写入 memory/YYYY-MM-DD.md
    │
    ▼
旧消息被压缩/截断
    │
    ▼
后续每轮 Auto-Recall → 语义搜索相关记忆并注入上下文
```

**混合搜索算法**：

```
最终得分 = 0.7 × 向量余弦相似度 + 0.3 × BM25 关键词得分
```

- **向量搜索**（70%权重）：语义理解，"网关主机"能匹配"运行 Gateway 的机器"
- **BM25 搜索**（30%权重）：精确匹配，擅长错误码、函数名等

**后处理**：MMR 重排序（lambda: 0.7，平衡相关性与多样性）+ 时间衰减（halfLife: 30天）

> [!abstract] 核心理解
> "无限记忆"不是真的无限存储，而是通过"压缩前主动刷写 + 语义搜索召回"的机制，让 AI 在有限的上下文窗口中模拟出无限记忆的效果。

> 交叉参考：→ P12 记忆系统架构详解（本系列最长一集） → P15 对话记忆管理系统

---

### P10：自由组装Skills功能实现策略（~9.7分钟）

**核心内容**：OpenClaw Skills 系统的模块化设计理念。

**Skills 的本质**：不是代码，而是**带 YAML frontmatter 的 Markdown 文件**。

```markdown
# SKILL.md 示例
---
name: hr-recruiter
description: AI HR 招聘助手技能
triggers:
  - "招聘"
  - "简历筛选"
  - "面试"
tools:
  - web_search
  - read
  - write
---

# HR 招聘助手

当用户要求招聘相关操作时：
1. 分析岗位需求，提取关键能力要求
2. 使用 web_search 搜索匹配候选人
3. 生成候选人评估报告
4. 输出面试问题清单
```

**Skills 设计原则**：
- **即插即用**：放入 `~/.openclaw/skills/` 目录即自动生效，不需重启
- **按需注入**：AI 不会加载所有 Skills，仅在消息匹配 triggers 时注入
- **社区生态**：ClawHub 已有 5,700+ 社区技能
- **安全审查**：约 12% 的社区技能被发现有恶意内容，需谨慎选择

> [!tip] Mini OpenClaw 的 Skills 简化思路
> 不需要实现完整的 trigger 匹配引擎，可以先用简单的关键词匹配 + 手动加载的方式，核心是理解"将能力模块化为独立文件"的设计思想。

> 交叉参考：→ P14 Skills 系统实现 → P22 插件与 Skills 深入

---

## 模块三：架构原理与Mini OpenClaw实现（P11-P18，约108分钟）

> [!info] 模块概要
> 本模块是整个系列的技术核心，深入讲解 OpenClaw 的架构原理（特别是记忆系统），并从零实现一个工业级的 Mini OpenClaw。P12 是全系列最长的一集（29分钟），也是技术含量最高的一集。

### 分集详解表

| 集数 | 标题 | 时长 | 核心要点 |
|------|------|------|----------|
| P11 | OpenClaw原理一站式精讲速通 | ~8分钟 | 架构原理总览 |
| P12 | OpenClaw自我迭代进化架构核心记忆系统架构详解 | ~29分钟 | 记忆系统核心（最长一集） |
| P13 | 从零到一搭建工业级智能体记忆系统——MiniOpenClaw | ~8.8分钟 | 工业级记忆系统搭建 |
| P14 | Mini OpenClaw的Agent Skills系统 | ~9分钟 | Skills 系统实现 |
| P15 | MiniOpenClaw对话记忆管理系统设计 | ~23.1分钟 | 对话记忆管理系统 |
| P16 | Mini-OpenClaw后端代码详解 | ~8.6分钟 | 后端代码逐行讲解 |
| P17 | Mini-OpenClaw开发需求文档 | ~6.7分钟 | 需求文档编写 |
| P18 | Mini-OpenClaw Readme文档（去广告） | ~14.9分钟 | README 文档 |

---

### P11：原理一站式精讲速通（~8分钟）

**核心内容**：OpenClaw 架构原理的高密度速通。

**三层架构速览**：

```
┌──────────────────────────────────────────────────┐
│              Channel 层（50+ 平台适配）              │
│  消息归一化 → StandardMessage 格式                   │
│  {userId, channelId, content, timestamp, metadata} │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│              Gateway 层（中央控制平面）               │
│  WebSocket 服务 · 会话管理 · 路由 · 认证 · 并发控制   │
│  六阶段消息处理流水线                                 │
│  默认绑定: ws://127.0.0.1:18789                     │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│              LLM Provider 层（可插拔模型）            │
│  provider/model 引用格式                             │
│  anthropic/claude-opus-4-6 · openai/gpt-5.3 等     │
└──────────────────────────────────────────────────┘
```

**六阶段消息处理流水线**：

```
消息进入 → ① 摄入 → ② 访问控制 → ③ 会话解析 → ④ 上下文组装 → ⑤ 模型调用 → ⑥ 响应投递
```

1. **摄入**：平台适配器解析原始消息
2. **访问控制**：白名单/配对码验证
3. **会话解析**：用 `{scope}-{agentId}-{identifier}` 键查找/创建会话
4. **上下文组装**：加载历史 + 系统提示词 + 语义搜索记忆 + Skills
5. **模型调用**：流式发送到 LLM，拦截工具调用并执行
6. **响应投递**：格式化后回流，持久化会话状态

**Agent 运行四阶段**：上下文组装 → 模型推理 → 工具执行 → 状态持久化

> [!tip] 本集定位
> 这是一个"地图集"，帮你建立全局视野。后续 P12 会深入记忆系统的每个细节。

> 交叉参考：→ P4 行业背景 → P12 记忆系统详解 → [[docs/OpenClaw 完整技术架构与应用详解.md|完整技术架构]]

---

### P12：记忆系统架构详解（~29分钟）★ 全系列最长

**核心内容**：OpenClaw 的核心创新——自我迭代进化的记忆系统。

> [!abstract] 本集重要性
> 这是全系列最长、技术含量最高的一集。记忆系统是 OpenClaw 与普通 AI 聊天最本质的区别，理解了记忆系统，就理解了 OpenClaw 80% 的技术本质。

**向量索引实现细节**：

```
存储后端：SQLite + sqlite-vec 扩展

数据库核心表结构：
┌────────────────┬──────────────────────────────┐
│ files          │ 跟踪哪些文件被索引              │
│ chunks         │ 文本块 + 对应向量               │
│ embedding_cache│ 缓存已计算的向量（避免重复计算）  │
│ chunks_fts     │ FTS5 全文搜索索引（BM25 用）    │
│ vec_chunks     │ 向量索引（语义搜索用）           │
└────────────────┴──────────────────────────────┘
```

**文本分块策略**：

```
长文档 → 切分为块
┌──────────┐  ┌──────────┐  ┌──────────┐
│  块 1     │  │  块 2     │  │  块 3     │
│ ~400 token│  │ ~400 token│  │ ~400 token│
│(~1600字符)│  │(~1600字符)│  │(~1600字符)│
└─────┬────┘  └─────┬────┘  └──────────┘
      └─重叠80token─┘
```

- 目标块大小：约 400 token（~1,600 字符）
- 块间重叠：80 token（~320 字符）——防止边界上下文丢失
- 每个块有 SHA-256 哈希用于缓存命中判断

**嵌入模型自动选择链**（优先级从高到低）：
1. 本地 GGUF 模型（`embeddinggemma-300m`，约 0.6GB，免费）
2. OpenAI `text-embedding-3-small`（1536 维）
3. Gemini `gemini-embedding-001`（768 维）
4. Voyage → Mistral → 禁用

**上下文窗口管理——压缩前记忆刷写的完整流程**：

```
对话进行中...
    │
    ├── 每轮结束检查 token 使用量
    │
    ├── 达到 80% 上下文窗口阈值（~176K / 200K token）
    │
    ▼
触发「静默」Agent 回合
    │
    ├── 系统注入特殊提示："你即将丢失上下文"
    │
    ├── AI 将以下信息提取到 memory/YYYY-MM-DD.md：
    │   ├── 重要决策与结论
    │   ├── 状态变化与关键事实
    │   ├── 经验教训
    │   └── 用户偏好更新
    │
    ├── 旧消息被压缩/截断
    │
    └── 后续每轮自动执行 Auto-Recall：
        └── 语义搜索记忆 → 注入相关片段到上下文
```

**"自我迭代进化"的含义**：
- 记忆不是静态存储，而是随每次对话**主动更新和优化**
- 通过 MMR 重排序和时间衰减，记忆系统会自动"遗忘"不重要的信息
- 新的经验会覆盖旧的、过时的知识
- 系统越用越"聪明"——因为积累的记忆越来越精准

> [!warning] 关键设计约束
> - `MEMORY.md`（持久记忆）仅在私信会话中加载，**群组中绝不暴露**——防止隐私泄露
> - 系统提示词文件（AGENTS.md）单文件上限 20,000 字符，总计上限 150,000 字符

> 交叉参考：→ P9 记忆策略总览 → P13 工业级实现 → P15 对话记忆管理

---

### P13：从零搭建工业级智能体记忆系统（~8.8分钟）

**核心内容**：将 P12 的理论付诸实践，搭建 Mini OpenClaw 的记忆系统。

**实现路线**：

```
Step 1: 搭建 SQLite + sqlite-vec 向量存储
Step 2: 实现文本分块器（400 token 块 + 80 token 重叠）
Step 3: 接入嵌入模型（推荐先用 OpenAI text-embedding-3-small）
Step 4: 实现混合搜索（向量 0.7 + BM25 0.3）
Step 5: 实现三层记忆的读写接口
Step 6: 实现压缩前刷写触发机制
```

**SQLite 向量索引的优势**：
- 无需额外安装数据库服务
- 单文件存储，便于备份和迁移
- `sqlite-vec` 扩展提供高效的 ANN（近似最近邻）搜索
- 对于个人/小规模使用场景完全够用

> [!tip] 实现建议
> 先实现最简版本（只有向量搜索），验证流程通了再加 BM25 混合搜索和 MMR 重排序。

---

### P14：Mini OpenClaw 的 Agent Skills 系统（~9分钟）

**核心内容**：Skills 系统的代码级实现。

**Skills 加载流程**：

```
启动时：
  扫描 skills/ 目录 → 解析 YAML frontmatter → 构建 trigger 索引

消息到达时：
  提取消息关键词 → 匹配 trigger → 找到相关 Skills → 注入系统提示词

关键设计：
  Skills 内容不会全部加载 → 只加载匹配的 → 节省 token
```

**YAML frontmatter 结构**：

```yaml
---
name: skill-name        # 技能标识
description: 技能描述     # 一句话描述
triggers:               # 触发关键词列表
  - keyword1
  - keyword2
tools:                  # 该技能需要的工具列表
  - web_search
  - read
---
```

> 交叉参考：→ P10 Skills 策略 → P22 插件与 Skills 深入

---

### P15：对话记忆管理系统设计（~23.1分钟）

**核心内容**：对话记忆的完整管理——上下文压缩、摘要生成、会话持久化。

> [!abstract] 本集重点
> 这是模块三中第二长的一集（23分钟），重点解决"长对话怎么管理"的工程问题。

**会话存储格式**：
- 持久化为 JSONL 文件：`~/.openclaw/sessions/{sessionId}.jsonl`
- 每行一个 JSON 编码的 `AgentMessage` 对象

**三层防护机制**：

```
┌──────────────────────────────────────────────┐
│  防护层 1：工具结果截断                         │
│  → 工具返回的超长结果被截断，防止单次爆炸         │
├──────────────────────────────────────────────┤
│  防护层 2：上下文窗口预防性压缩（80% 阈值）      │
│  → 在达到上限之前触发压缩前记忆刷写              │
├──────────────────────────────────────────────┤
│  防护层 3：会话修复                             │
│  → 损坏的会话文件可以自动修复                    │
└──────────────────────────────────────────────┘
```

**上下文压缩策略**：
- **摘要压缩**：将早期对话压缩为摘要，保留关键信息
- **滑动窗口**：只保留最近 N 轮对话的完整内容
- **重要消息置顶**：标记为"重要"的消息不被压缩

**并发控制**：
- 核心原则："同一 Session 串行，不同 Session 并行"
- 分布式部署使用 Redis redlock 分布式锁
- 防止同一用户的消息被并发处理导致上下文混乱

> 交叉参考：→ P9 记忆策略 → P12 记忆系统详解

---

### P16：Mini-OpenClaw 后端代码详解（~8.6分钟）

**核心内容**：Mini OpenClaw 后端代码的逐行讲解。

**核心模块拆解**：

```
mini-openclaw/
├── server.py (或 server.ts)    ← 主入口，HTTP/WebSocket 服务
├── agent/
│   ├── runtime.py              ← Agent 运行时（四阶段循环）
│   ├── context_builder.py      ← 上下文组装器
│   └── tool_executor.py        ← 工具执行器
├── memory/
│   ├── store.py                ← 三层记忆存储
│   ├── vector_index.py         ← SQLite 向量索引
│   └── search.py               ← 混合搜索（向量+BM25）
├── skills/
│   ├── loader.py               ← Skills 文件加载器
│   └── matcher.py              ← Trigger 匹配器
└── config/
    └── settings.py             ← 配置管理
```

**Agent 运行时核心循环**：

```python
# 伪代码示例
async def agent_loop(message, session):
    # Phase 1: 上下文组装
    context = build_context(session, message)
    relevant_memories = memory_search(message.content)
    relevant_skills = skill_match(message.content)

    # Phase 2: 模型推理
    response = await llm.stream(context + relevant_memories + relevant_skills)

    # Phase 3: 工具执行（如果模型请求了工具调用）
    while response.has_tool_calls:
        results = execute_tools(response.tool_calls)
        response = await llm.stream(context + results)

    # Phase 4: 状态持久化
    session.append(message, response)
    memory_update(session)
```

> 交叉参考：→ P13 记忆系统实现 → P14 Skills 实现

---

### P17：Mini-OpenClaw 开发需求文档（~6.7分钟）

**核心内容**：如何为 Mini OpenClaw 编写规范的开发需求文档。

- 需求文档的结构与要素
- 功能需求 vs 非功能需求
- 用户故事的编写方法
- 技术约束与边界条件
- 为后续 AI HR 实战打下文档基础

> [!tip] 文档驱动开发
> 赋范课堂强调"先写文档再写代码"的开发理念。好的需求文档不仅帮助开发，也为后续的 AI Agent 提供精确的任务描述。

---

### P18：Mini-OpenClaw Readme文档（~14.9分钟）

**核心内容**：项目 README 的编写规范与最佳实践。

- 项目简介与定位说明
- 快速开始指南（安装、配置、运行）
- 架构说明与核心概念
- API 文档与使用示例
- 贡献指南与许可证
- 去除不必要的广告内容，保持文档简洁

> 交叉参考：→ P17 需求文档 → P16 代码实现

---

## 模块四：AI HR 数字员工实战（P19-P28，约119分钟）

> [!info] 模块概要
> 本模块是系列的实战高潮部分，从 OpenClaw 基础架构回顾开始，逐步深入内置工具、插件、人格与记忆管理，最终完成一个企业可用的 AI HR 数字员工的开发与测试。P24（28分钟）和P25 共同构成实战开发的核心。

### 分集详解表

| 集数 | 标题 | 时长 | 核心要点 |
|------|------|------|----------|
| P19 | 手把手开发一个企业可用AI HR数字员工 | ~14分钟 | HR 数字员工开发入门 |
| P20 | OpenClaw基础架构与使用场景介绍 | ~11.3分钟 | 架构回顾 + 使用场景 |
| P21 | OpenClaw内置工具 | ~8.7分钟 | 内置工具用法详解 |
| P22 | 插件与Skills系统 | ~10.6分钟 | 插件生态 + Skills 深入 |
| P23 | OpenClaw人格与记忆管理系统 | ~10.1分钟 | 人设配置 + 记忆管理 |
| P24 | 实战：AI数字员工——AI HR 开发实战（上） | ~28.4分钟 | 核心开发流程（重点集） |
| P25 | 实战：AI数字员工——AI HR 开发实战（下） | ~8.8分钟 | 开发实战下篇 |
| P26 | 重新设置OpenClaw | ~8分钟 | 重置配置方法 |
| P27 | 音频转文字&PDF转MD功能实现 | ~10.2分钟 | 音频转文字、PDF 转 MD |
| P28 | OpenClaw-HR实战测试 | ~9.4分钟 | HR 数字员工实战测试 |

---

### P19：手把手开发AI HR数字员工（~14分钟）

**核心内容**：AI HR 数字员工项目的整体规划与入门。

**HR 数字员工的核心能力**：

```
┌──────────────────────────────────────────────┐
│              AI HR 数字员工能力矩阵             │
├──────────────┬───────────────────────────────┤
│ 简历筛选     │ 自动解析简历，匹配岗位要求         │
│ 面试安排     │ 协调候选人和面试官的日程            │
│ 候选人沟通   │ 自动发送面试通知、结果通知          │
│ 知识问答     │ 回答公司政策、福利、制度相关问题     │
│ 员工入职     │ 引导新员工完成入职流程              │
│ 数据分析     │ 招聘漏斗分析、人才市场洞察          │
└──────────────┴───────────────────────────────┘
```

**技术实现路线**：
- 使用 OpenClaw 作为 Agent 运行时
- 通过 Skills 定义 HR 业务逻辑
- 通过 Tools 实现简历解析、日程查询等能力
- 通过 Memory 记住候选人信息和沟通历史

> 交叉参考：→ P24-P25 核心开发实战 → P28 实战测试

---

### P20：基础架构与使用场景介绍（~11.3分钟）

**核心内容**：为实战做准备的架构回顾与场景分析。

**OpenClaw 在 HR 场景的应用映射**：

| OpenClaw 组件 | HR 场景应用 |
|--------------|-----------|
| Channel 层 | 候选人通过飞书/微信/邮件沟通 |
| Gateway 层 | 统一管理所有候选人会话和状态 |
| Provider 层 | 用 Claude 做深度分析，用便宜模型做日常沟通 |
| Memory 系统 | 记住每个候选人的信息、面试反馈、偏好 |
| Skills | HR 业务技能（简历筛选、面试安排等） |
| Tools | 简历解析、日程 API、邮件发送 |
| Cron | 定时扫描新简历、发送面试提醒 |

> 交叉参考：→ P11 架构原理 → P19 HR 项目规划

---

### P21：OpenClaw内置工具（~8.7分钟）

**核心内容**：OpenClaw 八大工具组的详细用法。

**八大工具组在 HR 场景的应用**：

| 工具组 | 工具 | HR 场景用法 |
|--------|------|-----------|
| `group:runtime` | `exec`, `bash` | 运行简历解析脚本 |
| `group:fs` | `read`, `write`, `edit` | 读写候选人档案文件 |
| `group:web` | `web_search`, `web_fetch` | 搜索候选人社交主页 |
| `group:ui` | `browser` | 自动操作招聘网站（CDP 协议） |
| `group:messaging` | `message` | 跨平台通知候选人 |
| `group:sessions` | `sessions_spawn` | 生成专门的面试评估 Agent |
| `group:memory` | `memory_search` | 搜索历史候选人记录 |
| `group:automation` | `cron` | 定时扫描新简历投递 |

**工具策略五级级联**：
1. 全局允许/拒绝列表
2. Provider 级覆盖
3. Agent 级覆盖
4. 沙箱策略
5. 仅所有者限制

> [!warning] 安全最佳实践
> HR Agent 处理敏感个人信息，务必配置工具权限白名单，限制 Agent 只能访问必要的工具。特别是 `exec` 和 `browser` 工具需要严格控制。

---

### P22：插件与Skills系统（~10.6分钟）

**核心内容**：OpenClaw 插件生态与 Skills 系统的深入讲解。

**四种插件类型**：

| 类型 | 说明 | HR 场景示例 |
|------|------|-----------|
| Channels | 消息平台集成 | 飞书/企业微信适配器 |
| Tools | 能力扩展 | 简历解析工具 |
| Providers | 模型推理 | 国内模型端点 |
| Memory | 搜索后端 | 自定义向量搜索 |

**MCP（Model Context Protocol）集成**：

```json
{
  "mcpServers": {
    "hr-database": {
      "command": "npx",
      "args": ["-y", "@company/hr-mcp-server"],
      "env": { "DB_URL": "sqlite:///hr.db" }
    }
  }
}
```

- MCP 协议基于 JSON-RPC 2.0 over stdio/HTTP
- 社区已有 1,000+ MCP 服务器
- 每个 Agent 可拥有独立的 MCP 服务器集合

> 交叉参考：→ P10 Skills 策略 → P14 Skills 实现

---

### P23：人格与记忆管理系统（~10.1分钟）

**核心内容**：Agent 人设配置与记忆管理的实操。

**核心配置文件矩阵**：

| 文件 | 作用 | 字符限制 | HR Agent 示例 |
|------|------|---------|-------------|
| `AGENTS.md` | 操作指令与行为规则 | 单文件 20,000 | "筛选简历时关注工作经验匹配度" |
| `SOUL.md` | 人格、语气、操作边界 | 总计 150,000 | "你是一个专业、友善的 HR 助手" |
| `USER.md` | 用户身份与偏好 | - | "公司是一家科技创业公司" |
| `IDENTITY.md` | Agent 名称、特征 | - | "你叫小招，是XX公司的 AI HR" |
| `HEARTBEAT.md` | 心跳检查清单 | - | "检查是否有新简历投递" |

**SOUL.md 示例（HR Agent）**：

```markdown
# HR Agent 人格设定

## 身份
你是 XX 公司的 AI HR 助手"小招"，专注于招聘和员工服务。

## 语气
- 专业但友善
- 对候选人保持尊重和耐心
- 对内部员工热情周到

## 操作边界
- 绝不泄露候选人的薪资期望给其他候选人
- 绝不在未授权的情况下做出录用决定
- 敏感操作（如发 offer）必须人工确认
```

> [!tip] 人格设计原则
> 好的人格设定不是写"你是一个好的 HR"，而是写"遇到 X 情况时，做 Y 而不是 Z"——越具体越好。

---

### P24：AI HR 开发实战（上）（~28.4分钟）★ 实战核心

**核心内容**：AI HR 数字员工的核心开发流程。

> [!abstract] 重要性
> 这是实战部分最关键的一集（28分钟），涵盖了从需求分析到代码实现的完整开发流程。

**开发流程**：

```
Step 1: 需求分析
│  明确 HR Agent 需要哪些能力
│
Step 2: Skills 编写
│  将 HR 业务能力拆分为独立的 SKILL.md 文件
│  ├── resume-screening.md (简历筛选)
│  ├── interview-scheduling.md (面试安排)
│  ├── candidate-communication.md (候选人沟通)
│  └── onboarding-guide.md (入职引导)
│
Step 3: 工具配置
│  配置 HR Agent 需要的工具权限
│  ├── read/write: 读写简历文件
│  ├── web_search: 搜索候选人信息
│  ├── message: 发送通知
│  └── cron: 定时任务
│
Step 4: 人格与记忆配置
│  编写 AGENTS.md / SOUL.md / USER.md
│
Step 5: 记忆系统初始化
│  导入公司基础知识（岗位描述、公司文化、招聘流程）
│
Step 6: 集成测试
│  模拟真实 HR 场景进行测试
```

**简历筛选 Skill 示例**：

```markdown
---
name: resume-screening
description: 智能简历筛选与评估
triggers:
  - "筛选简历"
  - "评估候选人"
  - "简历分析"
tools:
  - read
  - write
  - web_search
---

# 简历筛选技能

## 工作流程

1. 读取岗位描述文件（JD）
2. 读取候选人简历
3. 按以下维度评估匹配度：
   - 技术技能匹配（权重40%）
   - 工作经验相关性（权重30%）
   - 教育背景（权重15%）
   - 项目经验（权重15%）
4. 输出评估报告：评分 + 优势 + 风险点 + 面试建议
5. 将评估结果写入候选人档案

## 评分标准
- 90-100分：强烈推荐面试
- 70-89分：推荐面试
- 50-69分：待定，需人工复核
- 50分以下：不推荐
```

**多 Agent 协作在 HR 场景的应用**：

```
主 Agent（HR 协调员）
    │
    ├── spawn → 简历筛选 Agent（批量处理简历）
    │            使用便宜模型 → 降低成本
    │
    ├── spawn → 面试评估 Agent（深度候选人分析）
    │            使用强模型 → 保证质量
    │
    └── spawn → 沟通 Agent（候选人通知）
                 使用快速模型 → 保证响应速度
```

> 交叉参考：→ P19 HR 项目规划 → P25 实战下篇 → P28 实战测试

---

### P25：AI HR 开发实战（下）（~8.8分钟）

**核心内容**：实战开发的收尾工作。

- 候选人沟通模板的编写与配置
- 面试流程自动化的实现
- 心跳系统配置——定时扫描新简历投递
- 异常处理与边界情况
- 与上篇的功能整合与联调

**Cron 定时任务示例**：

```yaml
# 每天早上9点扫描新简历
cron: "0 9 * * *"
task: |
  检查招聘邮箱是否有新简历投递。
  如果有，自动执行简历筛选技能，生成评估报告。
  对于70分以上的候选人，自动发送面试邀请。
  将今日筛选结果整理成简报发送给HR负责人。
```

> 交叉参考：→ P24 实战上篇 → P28 测试

---

### P26：重新设置OpenClaw（~8分钟）

**核心内容**：如何重置 OpenClaw 配置，从零开始。

- 清除配置文件和记忆数据
- 重新运行引导向导
- 迁移已有的 Skills 和配置
- 常见配置问题的排查与解决

**重置命令**：

```bash
# 备份当前配置
cp -r ~/.openclaw ~/.openclaw.backup

# 重新运行引导
openclaw onboard --install-daemon

# 如需完全重置
rm -rf ~/.openclaw
openclaw onboard --install-daemon
```

> [!warning] 操作前务必备份
> 重置会清除所有记忆和会话历史。如果有重要数据，先执行备份。

---

### P27：音频转文字&PDF转MD功能实现（~10.2分钟）

**核心内容**：为 HR Agent 添加音频转文字和 PDF 转 Markdown 的实用功能。

**HR 场景应用**：
- **音频转文字**：将面试录音自动转为文字记录
- **PDF 转 MD**：将 PDF 格式的简历转为可分析的 Markdown 文本

**实现思路**：
- 音频转文字：对接 Whisper API / 讯飞语音等服务
- PDF 转 MD：使用 pdf-parse 等库提取文本，保留结构
- 将这些能力封装为 OpenClaw 工具或 Skills

> [!tip] 实用技巧
> 面试录音转文字 + 记忆系统 = 面试评估的"完美记忆"。AI 可以基于完整的面试记录进行候选人评估，比人工笔记更全面准确。

---

### P28：OpenClaw-HR 实战测试（~9.4分钟）

**核心内容**：对开发完成的 AI HR 数字员工进行全流程实战测试。

**测试场景覆盖**：

```
测试 1：简历筛选流程
│  投递简历 → Agent 自动解析 → 生成评估报告 → 验证评分准确性
│
测试 2：候选人沟通
│  候选人发消息 → Agent 自动回复 → 安排面试 → 发送通知
│
测试 3：记忆持久化
│  中断对话 → 重新开始 → 验证 Agent 仍记得候选人信息
│
测试 4：多 Agent 协作
│  主 Agent 分配任务 → 子 Agent 执行 → 结果汇总
│
测试 5：异常处理
│  无效简历 → 网络超时 → 模型不可用 → 验证 fallback 机制
```

**测试结果验证要点**：
- 简历筛选的准确率和一致性
- 候选人沟通的语气和专业度
- 记忆系统在长对话中的稳定性
- 定时任务的可靠执行
- 安全边界的有效性（不泄露敏感信息）

> 交叉参考：→ P24-P25 开发实战 → P19 HR 项目规划

---

## 学习路径建议

> [!abstract] 三条学习路径
> 根据你的时间和目标，选择最适合的路径。

### 路径一：快速入门（~1.5小时）

适合：想快速了解 OpenClaw 并跑通 Demo 的开发者。

```
P1 (1分钟) → P3 (5分钟) → P5 (10分钟) → P6 (10分钟)
→ P11 (8分钟) → P20 (11分钟) → P21 (9分钟) → P23 (10分钟)
→ P28 (9分钟)

总计：约73分钟（~1.2小时）
```

### 路径二：完整学习（~5.4小时）

适合：想全面掌握 OpenClaw 的开发者。

```
按顺序看完 P1-P28，总计约324分钟（~5.4小时）

建议分5天完成：
  Day 1: P1-P6（模块一 + 部署）
  Day 2: P7-P10（远程连接 + Mini 规划）
  Day 3: P11-P15（架构原理 + 记忆系统）★ 最重要的一天
  Day 4: P16-P22（代码 + 文档 + 工具）
  Day 5: P23-P28（人格 + HR实战 + 测试）
```

### 路径三：实战专注（~2小时）

适合：已有 OpenClaw 基础，想快速开发 HR Agent 的开发者。

```
P19 (14分钟) → P20 (11分钟) → P21 (9分钟) → P22 (11分钟)
→ P23 (10分钟) → P24 (28分钟) → P25 (9分钟) → P27 (10分钟)
→ P28 (9分钟)

总计：约111分钟（~1.9小时）
```

---

## 技术知识速查

### OpenClaw 核心架构速查表

```
┌─────────────────────────────────────────────────────────────────┐
│                    OpenClaw 核心架构速查                          │
├─────────────────┬───────────────────────────────────────────────┤
│ 三层架构         │ Channel → Gateway → LLM Provider              │
│ 消息流水线       │ 摄入→访问控制→会话解析→上下文组装→模型调用→响应投递 │
│ Agent 四阶段     │ 上下文组装 → 模型推理 → 工具执行 → 状态持久化     │
│ 记忆三层         │ 持久(MEMORY.md) / 临时(daily) / 会话(sessions)  │
│ 搜索算法         │ 0.7×向量余弦 + 0.3×BM25                       │
│ 向量存储         │ SQLite + sqlite-vec 扩展                      │
│ 文本分块         │ 400 token/块，80 token 重叠                   │
│ 核心创新         │ 压缩前记忆刷写（80%阈值触发）                   │
│ 工具系统         │ 八大组：runtime/fs/web/ui/messaging/sessions/  │
│                 │ memory/automation                              │
│ 工具权限         │ 五级级联：全局→Provider→Agent→沙箱→管理员        │
│ Skills 格式      │ YAML frontmatter + Markdown                   │
│ 通信协议         │ WebSocket (JSON 文本帧)                        │
│ 默认端口         │ ws://127.0.0.1:18789                          │
│ 并发控制         │ 同 Session 串行，不同 Session 并行(Redis redlock)│
│ 会话存储         │ JSONL 文件: ~/.openclaw/sessions/              │
│ 编排引擎         │ Lobster 工作流引擎（确定性 YAML 编排）           │
│ 多 Agent         │ sessions_spawn / sessions_send                │
│ MCP 协议         │ JSON-RPC 2.0 over stdio/HTTP                  │
│ 人格配置         │ AGENTS.md / SOUL.md / USER.md / IDENTITY.md   │
│ 主动触发         │ 心跳(30min) / Cron / Hooks / Webhooks         │
└─────────────────┴───────────────────────────────────────────────┘
```

### 关键命令清单

```bash
# 安装
npm install -g openclaw@latest

# 引导设置
openclaw onboard --install-daemon

# 开始对话
openclaw chat

# 查看状态
openclaw status

# 查看日志
openclaw logs

# 安装技能
openclaw skill install <skill-name>

# 列出已安装技能
openclaw skill list

# 重启守护进程
openclaw restart

# 查看配置
openclaw config show
```

### 配置文件结构

```jsonc
// ~/.openclaw/openclaw.json
{
  // 模型配置
  "models": {
    "default": "anthropic/claude-sonnet-4-20250514",
    "fallbacks": ["openai/gpt-4o", "google/gemini-2.5-pro"]
  },

  // Agent 配置
  "agents": {
    "defaults": {
      "name": "Hal",
      "model": "anthropic/claude-sonnet-4-20250514"
    }
  },

  // Channel 配置
  "channels": {
    "telegram": {
      "adapter": "telegram",
      "token": "your-bot-token"
    }
  },

  // MCP 服务器
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    }
  },

  // 安全配置
  "security": {
    "sandbox": "all",           // off | non-main | all
    "sandboxScope": "session"   // session | agent | shared
  }
}
```

---

## 相关笔记

- [[docs/OpenClaw 完整技术架构与应用详解.md|OpenClaw 完整技术架构与应用详解]] — 技术架构的完整参考文档
- [[Research/OpenClaw-技术原理拆解-小白版.md|OpenClaw 技术原理拆解（小白版）]] — 小白友好的技术原理拆解
- [[Research/AI-从零开始完整学习指南.md|AI 从零开始完整学习指南]] — AI 学习的完整路线图

---

> [!info] 文档信息
> - **创建日期**：2026-03-01
> - **视频来源**：B站 BV115AbzjENY（赋范课堂）
> - **总集数**：28集 | **总时长**：约5.4小时
> - **标签**：#AI #OpenClaw #Agent #视频攻略 #赋范课堂 #HR数字员工
