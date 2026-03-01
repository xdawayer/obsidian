---
title: OpenClaw HR 数字员工 — 项目工程设计
date: 2026-03-01
tags: [AI, OpenClaw, HR, 工程设计, Agent, 项目结构]
aliases: [HR Agent Engineering, HR数字员工工程]
---

# OpenClaw HR 数字员工 — 项目工程设计

> [!abstract] 文档概述
> 本文档是 **AI HR 数字员工** 的项目工程设计文档，包含完整的项目结构、核心配置文件、代码模板、开发环境搭建步骤和部署方案。
>
> **文档版本**：v1.0
> **最后更新**：2026-03-01
> **关联文档**：[[docs/OpenClaw-HR-Agent-PRD|HR Agent PRD]]

---

## 1. 项目目录结构

```
openclaw-hr-agent/
├── .openclaw/                    # OpenClaw 配置
│   ├── openclaw.json            # 主配置
│   ├── workspace/
│   │   ├── AGENTS.md            # HR Agent 操作指令
│   │   ├── SOUL.md              # HR Agent 人格设定
│   │   ├── USER.md              # 用户信息
│   │   ├── IDENTITY.md          # Agent 身份
│   │   └── TOOLS.md             # 工具使用指南
│   ├── skills/                  # 自定义技能
│   │   ├── resume-parser/
│   │   │   └── SKILL.md
│   │   ├── candidate-matcher/
│   │   │   └── SKILL.md
│   │   ├── interview-generator/
│   │   │   └── SKILL.md
│   │   └── email-drafter/
│   │       └── SKILL.md
│   └── MEMORY.md                # 持久记忆
├── backend/                     # Python 后端
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI 入口
│   │   ├── config.py            # 配置管理
│   │   ├── models/              # 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── candidate.py
│   │   │   ├── job.py
│   │   │   ├── interview.py
│   │   │   └── evaluation.py
│   │   ├── services/            # 业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── resume_parser.py
│   │   │   ├── candidate_matcher.py
│   │   │   ├── interview_service.py
│   │   │   ├── email_service.py
│   │   │   └── memory_service.py
│   │   ├── agents/              # Agent 定义
│   │   │   ├── __init__.py
│   │   │   ├── hr_agent.py
│   │   │   └── tools.py
│   │   ├── api/                 # API 路由
│   │   │   ├── __init__.py
│   │   │   ├── candidates.py
│   │   │   ├── jobs.py
│   │   │   ├── interviews.py
│   │   │   └── analytics.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── embeddings.py
│   │       └── text_processing.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_resume_parser.py
│   │   ├── test_candidate_matcher.py
│   │   └── test_hr_agent.py
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── Dockerfile
├── data/
│   ├── sample_resumes/
│   ├── job_templates/
│   └── interview_questions/
├── docs/
│   ├── api.md
│   └── deployment.md
├── scripts/
│   ├── setup.sh
│   └── seed_data.py
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

> [!tip] 目录结构说明
> - `.openclaw/` 目录遵循 OpenClaw 框架的标准配置结构
> - `backend/` 采用分层架构：API 路由 → 业务服务 → 数据模型
> - `data/` 存放种子数据和模板，便于开发和测试
> - `scripts/` 存放自动化脚本

---

## 2. 核心配置文件内容

### 2.1 openclaw.json

> [!info] OpenClaw 主配置文件

```json
{
  "$schema": "https://openclaw.dev/schemas/config.json",
  "version": "1.0",
  "agent": {
    "name": "慧招",
    "description": "AI HR 数字员工 — 智能招聘助理",
    "language": "zh-CN",
    "timezone": "Asia/Shanghai"
  },
  "model": {
    "provider": "anthropic",
    "name": "claude-sonnet-4-20250514",
    "temperature": 0.3,
    "max_tokens": 4096,
    "fallback": {
      "provider": "openai",
      "name": "gpt-4o",
      "temperature": 0.3,
      "max_tokens": 4096
    }
  },
  "memory": {
    "enabled": true,
    "backend": "sqlite",
    "path": ".openclaw/memory.db",
    "auto_summarize": true,
    "retention_days": 365
  },
  "channels": [
    {
      "type": "wechat_work",
      "enabled": true,
      "config": {
        "corp_id": "${WECHAT_CORP_ID}",
        "agent_id": "${WECHAT_AGENT_ID}",
        "secret": "${WECHAT_SECRET}",
        "token": "${WECHAT_TOKEN}",
        "encoding_aes_key": "${WECHAT_AES_KEY}"
      }
    },
    {
      "type": "feishu",
      "enabled": true,
      "config": {
        "app_id": "${FEISHU_APP_ID}",
        "app_secret": "${FEISHU_APP_SECRET}",
        "verification_token": "${FEISHU_VERIFY_TOKEN}",
        "encrypt_key": "${FEISHU_ENCRYPT_KEY}"
      }
    },
    {
      "type": "telegram",
      "enabled": false,
      "config": {
        "bot_token": "${TELEGRAM_BOT_TOKEN}"
      }
    },
    {
      "type": "api",
      "enabled": true,
      "config": {
        "host": "0.0.0.0",
        "port": 8080,
        "auth": {
          "type": "bearer",
          "token": "${API_AUTH_TOKEN}"
        }
      }
    }
  ],
  "tools": {
    "builtin": ["web_search", "code_interpreter", "file_manager"],
    "custom": [
      {
        "name": "resume_parse",
        "endpoint": "http://localhost:8000/api/v1/tools/resume-parse",
        "permission": "auto"
      },
      {
        "name": "candidate_search",
        "endpoint": "http://localhost:8000/api/v1/tools/candidate-search",
        "permission": "auto"
      },
      {
        "name": "candidate_match",
        "endpoint": "http://localhost:8000/api/v1/tools/candidate-match",
        "permission": "auto"
      },
      {
        "name": "email_draft",
        "endpoint": "http://localhost:8000/api/v1/tools/email-draft",
        "permission": "confirm"
      },
      {
        "name": "calendar_schedule",
        "endpoint": "http://localhost:8000/api/v1/tools/calendar-schedule",
        "permission": "confirm"
      }
    ]
  },
  "skills_dir": ".openclaw/skills",
  "workspace_dir": ".openclaw/workspace",
  "logging": {
    "level": "INFO",
    "file": "logs/openclaw.log",
    "max_size": "50MB",
    "retention": 30
  }
}
```

### 2.2 AGENTS.md

```markdown
# HR Agent 操作指令

## 角色
你是「慧招」，一名专业的 AI HR 数字员工。你隶属于公司人力资源部门，主要职责是协助 HR
团队完成招聘全流程的工作。

## 核心能力
1. **简历处理**：解析、分析和评估候选人简历
2. **人才匹配**：基于职位要求智能推荐合适的候选人
3. **面试支持**：生成面试问题、安排面试日程、收集反馈
4. **沟通协助**：起草各类招聘沟通邮件和消息
5. **数据分析**：生成招聘数据报表和洞察

## 工作流程

### 当收到新的招聘需求时
1. 确认职位的关键信息（职位名称、部门、要求、薪资范围）
2. 如信息不完整，主动询问缺失信息
3. 生成标准化的职位描述 (JD)
4. 在人才库中搜索匹配的候选人
5. 推荐 Top 候选人并说明推荐理由

### 当收到新的简历时
1. 调用简历解析工具提取结构化信息
2. 将候选人信息存入人才库
3. 自动匹配当前开放的职位
4. 如果匹配度高，主动通知相关 HR
5. 向候选人发送简历收到确认（需审批）

### 当需要安排面试时
1. 根据职位和候选人生成针对性面试问题
2. 查询面试官和候选人的可用时间
3. 提出面试时间建议
4. 获得确认后创建日历事件
5. 向所有参与者发送面试通知

### 当面试结束后
1. 收集面试官的评估反馈
2. 汇总所有面试官的意见
3. 生成候选人评估报告
4. 提供录用/拒绝建议及理由

## 行为准则
- **专业性**：使用专业但不冰冷的语气
- **隐私**：不泄露候选人的个人隐私信息给无关人员
- **公正**：基于能力和岗位匹配度评估，避免任何形式的偏见
- **透明**：所有推荐和评估都提供可解释的理由
- **审慎**：涉及发送消息、修改数据等操作时主动请求确认
- **主动**：发现异常情况（如候选人长期未跟进）主动提醒

## 限制
- 不能代替人做最终的录用决策
- 不能未经确认直接向候选人发送消息
- 不能访问或泄露薪资谈判的保密信息
- 不能绕过公司的审批流程
```

### 2.3 SOUL.md

```markdown
# 慧招 — AI HR 数字员工

## 身份
我是慧招，一名 AI HR 数字员工。我热爱帮助企业找到最合适的人才，也致力于为每
一位候选人提供最好的求职体验。

## 性格
- **专业严谨**：对招聘流程、劳动法规、面试方法论有深入的理解
- **温暖友善**：与人沟通时保持真诚和尊重，让每个人都感到被重视
- **高效务实**：以结果为导向，用最少的步骤完成任务
- **细心周到**：注意细节，不遗漏重要信息，主动补全缺失环节
- **客观公正**：基于事实和数据做判断，不受主观偏见影响

## 沟通风格
- 对 HR 同事：简洁高效，直奔主题，提供清晰的行动建议
- 对候选人：礼貌专业，富有人情味，让人感到被尊重
- 对管理层：数据驱动，结论先行，提供决策依据
- 在不确定时：坦诚告知局限，提供多个选项供选择

## 核心信念
- 人才是企业最宝贵的资源
- 每一位候选人都值得被认真对待
- 效率和人性化可以兼得
- 数据辅助决策，但尊重人的最终判断
- 持续学习和改进是专业精神的体现

## 语言偏好
- 默认使用简体中文
- 如果用户使用英语，自动切换为英语
- 技术术语保留英文原文（如 JD、ATS、Pipeline）
```

### 2.4 SKILL.md — resume-parser

```markdown
# 简历解析技能 (Resume Parser)

## 描述
解析上传的简历文件（PDF/DOCX/图片），提取结构化信息并存入人才库。

## 触发条件
- 用户上传简历文件
- 用户发送"解析简历"、"分析简历"等指令
- 用户粘贴简历文本内容

## 输入
- 简历文件（PDF / DOCX / PNG / JPG）
- 或简历文本内容

## 处理流程
1. 检测文件类型并提取文本内容
2. 调用 LLM 进行智能解析，提取以下字段：
   - 基本信息：姓名、联系方式、地址
   - 教育背景：学校、学历、专业、毕业时间
   - 工作经历：公司、职位、时间段、工作内容
   - 技能标签：编程语言、框架、工具、软技能
   - 项目经历：项目名称、角色、技术栈、成果
   - 证书/资质
   - 语言能力
3. 生成技能向量嵌入
4. 存入数据库
5. 自动匹配当前开放的职位

## 输出
- 结构化候选人信息（JSON）
- 匹配的职位列表（如有）
- 解析质量评估

## 工具调用
- `resume_parse`：调用后端简历解析 API
- `candidate_search`：检查是否为重复简历

## 示例对话
用户：帮我解析这份简历 [附件: 张三_简历.pdf]
慧招：好的，我来解析这份简历。

解析完成！以下是提取的关键信息：

**基本信息**
- 姓名：张三
- 手机：138****1234
- 邮箱：zhangsan@example.com

**教育背景**
- 北京大学 / 计算机科学 / 硕士 / 2018-2021

**工作经历**
- 字节跳动 / 高级后端工程师 / 2021-至今
- 阿里巴巴 / 后端工程师（实习）/ 2020-2021

**核心技能**
Python, Go, Kubernetes, PostgreSQL, Redis, gRPC

该候选人已存入人才库。我发现他与当前开放的「高级后端工程师」职位匹配度较高（评分 92/100），是否需要我详细分析？
```

### 2.5 SKILL.md — candidate-matcher

```markdown
# 候选人匹配技能 (Candidate Matcher)

## 描述
根据职位要求（JD）在人才库中搜索和匹配最合适的候选人，提供多维度评分和推荐理由。

## 触发条件
- 用户请求推荐候选人
- 用户发送"匹配候选人"、"找合适的人"等指令
- 新职位创建后自动触发

## 输入
- 职位 ID 或职位描述
- 可选：筛选条件（工作年限、学历、技能等）
- 可选：推荐数量（默认 10）

## 处理流程
1. 解析职位要求，提取关键匹配维度
2. 向量相似度搜索候选人
3. 多维度评分：
   - 技能匹配度 (40%)
   - 经验匹配度 (25%)
   - 教育匹配度 (15%)
   - 行业相关性 (10%)
   - 综合潜力 (10%)
4. 生成每位候选人的推荐理由
5. 排序并返回 Top N 候选人

## 输出
- 排名列表（包含评分和推荐理由）
- 匹配分析报告

## 工具调用
- `candidate_search`：搜索人才库
- `candidate_match`：执行匹配评分

## 评分说明
| 分数区间 | 匹配等级 | 建议操作 |
|----------|----------|----------|
| 90-100 | 高度匹配 | 优先安排面试 |
| 75-89  | 较好匹配 | 建议面试 |
| 60-74  | 一般匹配 | 备选 |
| < 60   | 匹配度低 | 暂不推荐 |
```

### 2.6 requirements.txt

```txt
# Web Framework
fastapi==0.115.6
uvicorn[standard]==0.34.0
python-multipart==0.0.18

# Database
sqlalchemy==2.0.36
asyncpg==0.30.0
alembic==1.14.1

# AI / LLM
langchain==0.3.14
langchain-openai==0.3.0
langchain-anthropic==0.3.5
langchain-community==0.3.14
langgraph==0.2.60
openai==1.58.1
anthropic==0.40.0

# Vector Database
chromadb==0.5.23
sentence-transformers==3.3.1

# Document Processing
pypdf==5.1.0
python-docx==1.1.2
Pillow==11.0.0
pytesseract==0.3.13

# Data Validation
pydantic==2.10.4
pydantic-settings==2.7.1
email-validator==2.2.0

# HTTP Client
httpx==0.28.1
aiohttp==3.11.11

# Auth
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Utilities
python-dotenv==1.0.1
structlog==24.4.0
tenacity==9.0.0
jinja2==3.1.5

# Testing
pytest==8.3.4
pytest-asyncio==0.24.0
pytest-cov==6.0.0
httpx==0.28.1

# Linting (dev)
ruff==0.8.6
mypy==1.14.1
```

### 2.7 .env.example

```bash
# ============================================================
# OpenClaw HR Agent — 环境变量配置
# ============================================================
# 复制此文件为 .env 并填入实际值
# cp .env.example .env

# ---- 应用配置 ----
APP_NAME=openclaw-hr-agent
APP_ENV=development          # development | staging | production
APP_DEBUG=true
APP_HOST=0.0.0.0
APP_PORT=8000
SECRET_KEY=your-secret-key-change-in-production

# ---- 数据库配置 ----
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/hr_agent
DATABASE_ECHO=false

# ---- LLM 配置 ----
# Anthropic (推荐)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
ANTHROPIC_MODEL=claude-sonnet-4-20250514

# OpenAI (备用)
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o

# DeepSeek (可选)
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx
DEEPSEEK_MODEL=deepseek-chat

# 默认 LLM Provider
DEFAULT_LLM_PROVIDER=anthropic

# ---- 向量数据库配置 ----
CHROMA_HOST=localhost
CHROMA_PORT=8001
CHROMA_COLLECTION=hr_candidates
EMBEDDING_MODEL=text-embedding-3-small

# ---- OpenClaw 配置 ----
OPENCLAW_GATEWAY_URL=http://localhost:8080
OPENCLAW_API_TOKEN=your-openclaw-token

# ---- 企业微信配置 ----
WECHAT_CORP_ID=
WECHAT_AGENT_ID=
WECHAT_SECRET=
WECHAT_TOKEN=
WECHAT_AES_KEY=

# ---- 飞书配置 ----
FEISHU_APP_ID=
FEISHU_APP_SECRET=
FEISHU_VERIFY_TOKEN=
FEISHU_ENCRYPT_KEY=

# ---- Telegram 配置 ----
TELEGRAM_BOT_TOKEN=

# ---- 邮件配置 ----
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM=hr@example.com

# ---- 日志配置 ----
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# ---- Redis (可选，用于缓存) ----
REDIS_URL=redis://localhost:6379/0
```

### 2.8 docker-compose.yml

```yaml
version: "3.9"

services:
  # ---- HR Agent 后端服务 ----
  app:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: hr-agent-app
    ports:
      - "8000:8000"
    env_file:
      - .env
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/hr_agent
      - CHROMA_HOST=chromadb
      - CHROMA_PORT=8000
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      chromadb:
        condition: service_started
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./.openclaw:/app/.openclaw
    restart: unless-stopped
    networks:
      - hr-agent-network

  # ---- PostgreSQL 数据库 ----
  db:
    image: postgres:16-alpine
    container_name: hr-agent-db
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: hr_agent
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - hr-agent-network

  # ---- ChromaDB 向量数据库 ----
  chromadb:
    image: chromadb/chroma:0.5.23
    container_name: hr-agent-chromadb
    ports:
      - "8001:8000"
    volumes:
      - chromadata:/chroma/chroma
    environment:
      - IS_PERSISTENT=TRUE
      - ANONYMIZED_TELEMETRY=FALSE
    restart: unless-stopped
    networks:
      - hr-agent-network

  # ---- Redis 缓存 (可选) ----
  redis:
    image: redis:7-alpine
    container_name: hr-agent-redis
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data
    restart: unless-stopped
    networks:
      - hr-agent-network

volumes:
  pgdata:
  chromadata:
  redisdata:

networks:
  hr-agent-network:
    driver: bridge
```

### 2.9 pyproject.toml

```toml
[project]
name = "openclaw-hr-agent"
version = "0.1.0"
description = "AI HR 数字员工 — 基于 OpenClaw 的智能招聘助理"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
authors = [
    { name = "HR Agent Team", email = "team@example.com" },
]

dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.34.0",
    "sqlalchemy>=2.0.36",
    "asyncpg>=0.30.0",
    "alembic>=1.14.0",
    "langchain>=0.3.14",
    "langchain-openai>=0.3.0",
    "langchain-anthropic>=0.3.5",
    "chromadb>=0.5.23",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.7.0",
    "python-dotenv>=1.0.0",
    "httpx>=0.28.0",
    "pypdf>=5.1.0",
    "python-docx>=1.1.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "structlog>=24.4.0",
    "tenacity>=9.0.0",
    "jinja2>=3.1.5",
    "python-multipart>=0.0.18",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=6.0.0",
    "ruff>=0.8.0",
    "mypy>=1.14.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "SIM"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
```

---

## 3. 核心代码模板

### 3.1 main.py — FastAPI 应用入口

```python
"""
OpenClaw HR Agent — FastAPI 应用入口
"""
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import analytics, candidates, interviews, jobs
from app.config import settings

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("HR Agent 服务启动中...", env=settings.APP_ENV)

    # 初始化数据库连接
    from app.models import init_db
    await init_db()
    logger.info("数据库连接已建立")

    # 初始化向量数据库
    from app.services.candidate_matcher import CandidateMatcher
    matcher = CandidateMatcher()
    await matcher.initialize()
    logger.info("向量数据库已初始化")

    yield

    # 清理资源
    logger.info("HR Agent 服务关闭中...")
    from app.models import close_db
    await close_db()


app = FastAPI(
    title="OpenClaw HR Agent API",
    description="AI HR 数字员工 — 智能招聘助理后端服务",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(candidates.router, prefix="/api/v1/candidates", tags=["候选人管理"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["职位管理"])
app.include_router(interviews.router, prefix="/api/v1/interviews", tags=["面试管理"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["数据分析"])


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "openclaw-hr-agent",
        "version": "0.1.0",
    }


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用 OpenClaw HR Agent API",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
```

### 3.2 config.py — 配置管理

```python
"""
应用配置管理 — 基于 pydantic-settings
"""
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类，从环境变量和 .env 文件加载"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # ---- 应用配置 ----
    APP_NAME: str = "openclaw-hr-agent"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    SECRET_KEY: str = "change-me-in-production"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    # ---- 数据库配置 ----
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/hr_agent"
    DATABASE_ECHO: bool = False

    # ---- LLM 配置 ----
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-sonnet-4-20250514"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEFAULT_LLM_PROVIDER: str = "anthropic"

    # ---- 向量数据库 ----
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
    CHROMA_COLLECTION: str = "hr_candidates"
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    # ---- OpenClaw ----
    OPENCLAW_GATEWAY_URL: str = "http://localhost:8080"
    OPENCLAW_API_TOKEN: str = ""

    # ---- 邮件 ----
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "hr@example.com"

    # ---- 日志 ----
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    # ---- Redis ----
    REDIS_URL: str = "redis://localhost:6379/0"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    def get_llm_config(self) -> dict:
        """根据默认 Provider 返回 LLM 配置"""
        configs = {
            "anthropic": {
                "api_key": self.ANTHROPIC_API_KEY,
                "model": self.ANTHROPIC_MODEL,
            },
            "openai": {
                "api_key": self.OPENAI_API_KEY,
                "model": self.OPENAI_MODEL,
            },
            "deepseek": {
                "api_key": self.DEEPSEEK_API_KEY,
                "model": self.DEEPSEEK_MODEL,
            },
        }
        return configs.get(self.DEFAULT_LLM_PROVIDER, configs["anthropic"])


settings = Settings()
```

### 3.3 candidate.py — 候选人数据模型

```python
"""
候选人数据模型 — SQLAlchemy ORM + Pydantic Schema
"""
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase


# ============================================================
# SQLAlchemy ORM 模型
# ============================================================

class Base(DeclarativeBase):
    pass


class CandidateStatus(str, Enum):
    """候选人状态枚举"""
    NEW = "new"                    # 新建
    SCREENING = "screening"        # 筛选中
    INTERVIEW = "interview"        # 面试中
    OFFER = "offer"                # Offer 阶段
    HIRED = "hired"                # 已录用
    REJECTED = "rejected"          # 已拒绝
    WITHDRAWN = "withdrawn"        # 候选人撤回
    ARCHIVED = "archived"          # 已归档


class CandidateORM(Base):
    """候选人数据库模型"""
    __tablename__ = "candidates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    resume_url = Column(Text, nullable=True)
    resume_text = Column(Text, nullable=True)
    skills = Column(JSONB, default=list)
    experience_years = Column(Integer, default=0)
    education = Column(String(50), nullable=True)
    current_company = Column(String(200), nullable=True)
    current_title = Column(String(200), nullable=True)
    status = Column(String(20), default=CandidateStatus.NEW.value, index=True)
    tags = Column(JSONB, default=list)
    source = Column(String(50), nullable=True)
    extra_data = Column(JSONB, default=dict)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# ============================================================
# Pydantic Schema（请求/响应模型）
# ============================================================

class CandidateCreate(BaseModel):
    """创建候选人请求"""
    name: str = Field(..., min_length=1, max_length=100, description="候选人姓名")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    skills: List[str] = Field(default_factory=list, description="技能标签")
    experience_years: int = Field(0, ge=0, le=50, description="工作年限")
    education: Optional[str] = Field(None, description="最高学历")
    current_company: Optional[str] = Field(None, description="当前公司")
    current_title: Optional[str] = Field(None, description="当前职位")
    source: Optional[str] = Field(None, description="简历来源")
    tags: List[str] = Field(default_factory=list, description="自定义标签")


class CandidateUpdate(BaseModel):
    """更新候选人请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    skills: Optional[List[str]] = None
    experience_years: Optional[int] = Field(None, ge=0, le=50)
    education: Optional[str] = None
    current_company: Optional[str] = None
    current_title: Optional[str] = None
    status: Optional[CandidateStatus] = None
    tags: Optional[List[str]] = None


class CandidateResponse(BaseModel):
    """候选人响应"""
    id: uuid.UUID
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []
    experience_years: int = 0
    education: Optional[str] = None
    current_company: Optional[str] = None
    current_title: Optional[str] = None
    status: str
    tags: List[str] = []
    source: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CandidateMatchResult(BaseModel):
    """候选人匹配结果"""
    candidate: CandidateResponse
    overall_score: float = Field(..., ge=0, le=100, description="综合评分")
    skill_score: float = Field(..., ge=0, le=100, description="技能匹配度")
    experience_score: float = Field(..., ge=0, le=100, description="经验匹配度")
    education_score: float = Field(..., ge=0, le=100, description="教育匹配度")
    match_reason: str = Field(..., description="推荐理由")
    match_level: str = Field(..., description="匹配等级")


class CandidateSearchRequest(BaseModel):
    """候选人搜索请求"""
    query: str = Field(..., min_length=1, description="搜索查询（自然语言）")
    filters: Optional[Dict[str, Any]] = Field(None, description="过滤条件")
    limit: int = Field(10, ge=1, le=100, description="返回数量")
```

### 3.4 job.py — 职位数据模型

```python
"""
职位数据模型
"""
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.models.candidate import Base


class JobStatus(str, Enum):
    """职位状态"""
    DRAFT = "draft"
    OPEN = "open"
    PAUSED = "paused"
    CLOSED = "closed"
    FILLED = "filled"


class JobType(str, Enum):
    """职位类型"""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    INTERN = "intern"
    CONTRACT = "contract"


class JobORM(Base):
    """职位数据库模型"""
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False, index=True)
    department = Column(String(100), nullable=True)
    description = Column(Text, nullable=False)
    requirements = Column(JSONB, default=dict)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    location = Column(String(100), nullable=True)
    job_type = Column(String(20), default=JobType.FULL_TIME.value)
    status = Column(String(20), default=JobStatus.DRAFT.value, index=True)
    headcount = Column(Integer, default=1)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    extra_data = Column(JSONB, default=dict)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class JobCreate(BaseModel):
    """创建职位请求"""
    title: str = Field(..., min_length=1, max_length=200, description="职位名称")
    department: Optional[str] = Field(None, description="所属部门")
    description: str = Field(..., min_length=10, description="职位描述")
    requirements: Dict[str, Any] = Field(default_factory=dict, description="岗位要求")
    salary_min: Optional[int] = Field(None, ge=0, description="薪资下限（月薪/K）")
    salary_max: Optional[int] = Field(None, ge=0, description="薪资上限（月薪/K）")
    location: Optional[str] = Field(None, description="工作地点")
    job_type: JobType = Field(JobType.FULL_TIME, description="职位类型")
    headcount: int = Field(1, ge=1, description="招聘人数")


class JobResponse(BaseModel):
    """职位响应"""
    id: uuid.UUID
    title: str
    department: Optional[str] = None
    description: str
    requirements: Dict[str, Any] = {}
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    location: Optional[str] = None
    job_type: str
    status: str
    headcount: int = 1
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

### 3.5 hr_agent.py — LangChain Agent 定义

```python
"""
HR Agent — 基于 LangChain 的智能招聘助理
"""
from typing import Any, Dict, List, Optional

import structlog
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from app.agents.tools import (
    candidate_match_tool,
    candidate_search_tool,
    email_draft_tool,
    interview_questions_tool,
    resume_parse_tool,
)
from app.config import settings

logger = structlog.get_logger()

# ---- System Prompt (SOUL.md + AGENTS.md 合并) ----
SYSTEM_PROMPT = """你是「慧招」，一名专业的 AI HR 数字员工。

## 性格
- 专业严谨，对招聘流程有深入理解
- 温暖友善，尊重每一位候选人
- 高效务实，以结果为导向
- 客观公正，基于数据做判断

## 核心能力
1. 简历解析与分析
2. 候选人智能匹配与推荐
3. 面试问题生成
4. 招聘沟通文案起草
5. 人才库搜索

## 行为准则
- 所有推荐都提供可解释的理由
- 涉及发送消息、修改数据时主动请求确认
- 不确定时坦诚告知并询问
- 保护候选人隐私信息

## 当前时间
{current_time}
"""


def get_llm(provider: Optional[str] = None):
    """获取 LLM 实例"""
    provider = provider or settings.DEFAULT_LLM_PROVIDER

    if provider == "anthropic":
        return ChatAnthropic(
            model=settings.ANTHROPIC_MODEL,
            api_key=settings.ANTHROPIC_API_KEY,
            temperature=0.3,
            max_tokens=4096,
        )
    elif provider == "openai":
        return ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=0.3,
            max_tokens=4096,
        )
    else:
        raise ValueError(f"不支持的 LLM Provider: {provider}")


def create_hr_agent(
    provider: Optional[str] = None,
    memory: Optional[ConversationBufferWindowMemory] = None,
) -> AgentExecutor:
    """
    创建 HR Agent 实例

    Args:
        provider: LLM 提供商（anthropic / openai）
        memory: 对话记忆

    Returns:
        AgentExecutor 实例
    """
    llm = get_llm(provider)

    # 定义工具集
    tools = [
        resume_parse_tool,
        candidate_search_tool,
        candidate_match_tool,
        interview_questions_tool,
        email_draft_tool,
    ]

    # 构建 Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    # 创建 Agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # 对话记忆
    if memory is None:
        memory = ConversationBufferWindowMemory(
            k=20,
            memory_key="chat_history",
            return_messages=True,
        )

    # 创建 AgentExecutor
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=settings.APP_DEBUG,
        max_iterations=10,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
    )

    logger.info("HR Agent 已创建", provider=provider or settings.DEFAULT_LLM_PROVIDER)
    return executor


async def chat_with_agent(
    agent: AgentExecutor,
    message: str,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    与 HR Agent 对话

    Args:
        agent: AgentExecutor 实例
        message: 用户消息
        context: 额外上下文

    Returns:
        Agent 响应
    """
    from datetime import datetime

    input_data = {
        "input": message,
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    if context:
        input_data.update(context)

    try:
        result = await agent.ainvoke(input_data)
        logger.info(
            "Agent 对话完成",
            input_length=len(message),
            output_length=len(result.get("output", "")),
            steps=len(result.get("intermediate_steps", [])),
        )
        return {
            "output": result["output"],
            "intermediate_steps": [
                {
                    "tool": step[0].tool,
                    "input": str(step[0].tool_input),
                    "output": str(step[1]),
                }
                for step in result.get("intermediate_steps", [])
            ],
        }
    except Exception as e:
        logger.error("Agent 对话失败", error=str(e))
        return {
            "output": f"抱歉，处理您的请求时出现了问题：{str(e)}。请稍后重试。",
            "intermediate_steps": [],
            "error": str(e),
        }
```

### 3.6 tools.py — 自定义工具

```python
"""
HR Agent 自定义工具集
"""
import json
from typing import Any, Dict, List, Optional

import structlog
from langchain_core.tools import tool

logger = structlog.get_logger()


@tool
async def resume_parse_tool(file_path: str) -> str:
    """
    解析简历文件，提取候选人结构化信息。

    支持的文件格式：PDF、DOCX、PNG、JPG
    输入：简历文件路径
    输出：结构化的候选人信息（JSON格式）
    """
    from app.services.resume_parser import ResumeParser

    parser = ResumeParser()
    try:
        result = await parser.parse(file_path)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error("简历解析失败", file_path=file_path, error=str(e))
        return f"简历解析失败：{str(e)}"


@tool
async def candidate_search_tool(query: str, limit: int = 10) -> str:
    """
    在人才库中搜索候选人。

    支持自然语言查询，例如：
    - "有3年以上Python经验的后端工程师"
    - "985学历的产品经理"
    - "在字节跳动或阿里巴巴工作过的候选人"

    输入：搜索查询文本，返回数量限制
    输出：匹配的候选人列表
    """
    from app.services.candidate_matcher import CandidateMatcher

    matcher = CandidateMatcher()
    try:
        results = await matcher.search(query, limit=limit)
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error("候选人搜索失败", query=query, error=str(e))
        return f"搜索失败：{str(e)}"


@tool
async def candidate_match_tool(job_id: str, top_n: int = 10) -> str:
    """
    根据职位要求匹配最合适的候选人。

    输入：职位ID，返回的候选人数量
    输出：排名列表，包含评分和推荐理由
    """
    from app.services.candidate_matcher import CandidateMatcher

    matcher = CandidateMatcher()
    try:
        results = await matcher.match_for_job(job_id, top_n=top_n)
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error("候选人匹配失败", job_id=job_id, error=str(e))
        return f"匹配失败：{str(e)}"


@tool
async def interview_questions_tool(
    job_title: str,
    candidate_summary: str,
    question_count: int = 10,
    interview_type: str = "comprehensive",
) -> str:
    """
    根据职位和候选人信息生成面试问题。

    面试类型：
    - technical：技术面试
    - behavioral：行为面试（STAR方法）
    - cultural：文化匹配面试
    - comprehensive：综合面试（包含以上三种）

    输入：职位名称、候选人摘要、问题数量、面试类型
    输出：面试问题列表（含评分标准）
    """
    from app.services.interview_service import InterviewService

    service = InterviewService()
    try:
        questions = await service.generate_questions(
            job_title=job_title,
            candidate_summary=candidate_summary,
            count=question_count,
            interview_type=interview_type,
        )
        return json.dumps(questions, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error("面试问题生成失败", error=str(e))
        return f"面试问题生成失败：{str(e)}"


@tool
async def email_draft_tool(
    template_type: str,
    candidate_name: str,
    job_title: str,
    extra_info: Optional[str] = None,
) -> str:
    """
    起草招聘相关的邮件或消息。

    模板类型：
    - screening_pass：初筛通过通知
    - interview_invite：面试邀请
    - interview_reminder：面试提醒
    - offer：录用通知
    - rejection：婉拒信
    - follow_up：跟进消息

    输入：模板类型、候选人姓名、职位名称、额外信息
    输出：邮件/消息草稿
    """
    from app.services.email_service import EmailService

    service = EmailService()
    try:
        draft = await service.draft_email(
            template_type=template_type,
            candidate_name=candidate_name,
            job_title=job_title,
            extra_info=extra_info,
        )
        return json.dumps(draft, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error("邮件起草失败", error=str(e))
        return f"邮件起草失败：{str(e)}"
```

### 3.7 resume_parser.py — 简历解析服务

```python
"""
简历解析服务 — 使用 LLM 智能提取简历结构化信息
"""
import os
from pathlib import Path
from typing import Any, Dict, Optional

import structlog
from langchain_core.messages import HumanMessage

from app.config import settings

logger = structlog.get_logger()

# 简历解析 Prompt
RESUME_PARSE_PROMPT = """你是一位专业的简历解析专家。请仔细阅读以下简历内容，提取所有关键信息并以 JSON 格式返回。

## 简历内容
{resume_text}

## 输出格式要求
请严格按照以下 JSON 格式输出，不要添加额外说明：

```json
{{
  "name": "姓名",
  "email": "邮箱",
  "phone": "手机号",
  "location": "所在城市",
  "education": [
    {{
      "school": "学校名称",
      "degree": "学历（本科/硕士/博士）",
      "major": "专业",
      "start_year": 2018,
      "end_year": 2022,
      "gpa": "GPA（如有）"
    }}
  ],
  "work_experience": [
    {{
      "company": "公司名称",
      "title": "职位",
      "start_date": "2022-01",
      "end_date": "至今",
      "description": "工作职责描述",
      "highlights": ["工作亮点1", "工作亮点2"]
    }}
  ],
  "skills": ["技能1", "技能2", "技能3"],
  "projects": [
    {{
      "name": "项目名称",
      "role": "角色",
      "tech_stack": ["技术1", "技术2"],
      "description": "项目描述",
      "achievements": "项目成果"
    }}
  ],
  "certifications": ["证书1", "证书2"],
  "languages": ["中文-母语", "英语-流利"],
  "summary": "一句话总结候选人的核心竞争力",
  "experience_years": 5,
  "highest_education": "硕士",
  "current_company": "当前公司",
  "current_title": "当前职位"
}}
```
"""


class ResumeParser:
    """简历解析服务"""

    def __init__(self):
        from app.agents.hr_agent import get_llm
        self.llm = get_llm()

    async def parse(self, file_path: str) -> Dict[str, Any]:
        """
        解析简历文件

        Args:
            file_path: 简历文件路径

        Returns:
            结构化候选人信息
        """
        logger.info("开始解析简历", file_path=file_path)

        # 1. 提取文本内容
        text = await self._extract_text(file_path)
        if not text or len(text.strip()) < 50:
            raise ValueError("简历内容过少，无法解析。请检查文件是否正确。")

        # 2. LLM 智能解析
        result = await self._llm_parse(text)

        # 3. 验证和清洗
        result = self._validate_and_clean(result)

        logger.info("简历解析完成", candidate_name=result.get("name", "未知"))
        return result

    async def _extract_text(self, file_path: str) -> str:
        """从文件中提取文本"""
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return await self._extract_from_pdf(file_path)
        elif suffix in (".docx", ".doc"):
            return await self._extract_from_docx(file_path)
        elif suffix in (".png", ".jpg", ".jpeg"):
            return await self._extract_from_image(file_path)
        elif suffix == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise ValueError(f"不支持的文件格式：{suffix}")

    async def _extract_from_pdf(self, file_path: str) -> str:
        """从 PDF 提取文本"""
        from pypdf import PdfReader

        reader = PdfReader(file_path)
        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        return "\n".join(text_parts)

    async def _extract_from_docx(self, file_path: str) -> str:
        """从 DOCX 提取文本"""
        from docx import Document

        doc = Document(file_path)
        text_parts = []
        for para in doc.paragraphs:
            if para.text.strip():
                text_parts.append(para.text)

        # 也提取表格中的内容
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_text:
                    text_parts.append(row_text)

        return "\n".join(text_parts)

    async def _extract_from_image(self, file_path: str) -> str:
        """从图片提取文本（OCR）"""
        try:
            import pytesseract
            from PIL import Image

            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang="chi_sim+eng")
            return text
        except ImportError:
            raise ValueError("图片OCR功能需要安装 pytesseract 和 Tesseract-OCR")

    async def _llm_parse(self, text: str) -> Dict[str, Any]:
        """使用 LLM 解析简历文本"""
        import json

        prompt = RESUME_PARSE_PROMPT.format(resume_text=text[:8000])
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])

        # 提取 JSON
        content = response.content
        # 尝试从 markdown code block 中提取
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0].strip()
        else:
            json_str = content.strip()

        return json.loads(json_str)

    def _validate_and_clean(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """验证和清洗解析结果"""
        # 确保必要字段存在
        data.setdefault("name", "未知")
        data.setdefault("skills", [])
        data.setdefault("experience_years", 0)
        data.setdefault("education", [])
        data.setdefault("work_experience", [])

        # 清洗手机号和邮箱中的空格
        if data.get("phone"):
            data["phone"] = data["phone"].replace(" ", "").replace("-", "")
        if data.get("email"):
            data["email"] = data["email"].strip().lower()

        return data
```

### 3.8 candidate_matcher.py — 候选人匹配服务

```python
"""
候选人匹配服务 — 基于向量搜索 + LLM 评估的智能匹配
"""
import json
from typing import Any, Dict, List, Optional

import structlog
from langchain_core.messages import HumanMessage

from app.config import settings

logger = structlog.get_logger()

# 匹配评分 Prompt
MATCH_EVALUATION_PROMPT = """你是一位资深的人才匹配专家。请根据以下职位要求和候选人信息，进行多维度匹配评分。

## 职位要求
{job_description}

## 候选人信息
{candidate_info}

## 评分要求
请从以下维度进行 0-100 分的评分，并给出评分理由：

1. **技能匹配度** (权重 40%)：候选人技能与职位要求的匹配程度
2. **经验匹配度** (权重 25%)：工作年限、行业经验、项目经验
3. **教育匹配度** (权重 15%)：学历、专业相关性
4. **行业相关性** (权重 10%)：行业背景、公司背景
5. **综合潜力** (权重 10%)：成长轨迹、学习能力、综合素质

请严格以 JSON 格式输出：
```json
{{
  "skill_score": 85,
  "experience_score": 78,
  "education_score": 90,
  "industry_score": 70,
  "potential_score": 82,
  "overall_score": 82.3,
  "match_level": "较好匹配",
  "match_reason": "一段简洁的推荐理由",
  "strengths": ["优势1", "优势2"],
  "concerns": ["关注点1"]
}}
```
"""


class CandidateMatcher:
    """候选人匹配服务"""

    def __init__(self):
        self._chroma_client = None
        self._collection = None

    async def initialize(self):
        """初始化向量数据库连接"""
        import chromadb

        self._chroma_client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
        )
        self._collection = self._chroma_client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(
            "ChromaDB 初始化完成",
            collection=settings.CHROMA_COLLECTION,
            count=self._collection.count(),
        )

    async def add_candidate(
        self,
        candidate_id: str,
        resume_text: str,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        将候选人添加到向量数据库

        Args:
            candidate_id: 候选人 ID
            resume_text: 简历全文
            metadata: 元数据（姓名、技能等）
        """
        if self._collection is None:
            await self.initialize()

        self._collection.upsert(
            ids=[candidate_id],
            documents=[resume_text],
            metadatas=[metadata or {}],
        )
        logger.info("候选人已添加到向量库", candidate_id=candidate_id)

    async def search(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        语义搜索候选人

        Args:
            query: 搜索查询（自然语言）
            limit: 返回数量
            filters: 过滤条件

        Returns:
            匹配的候选人列表
        """
        if self._collection is None:
            await self.initialize()

        where_filter = None
        if filters:
            where_filter = self._build_chroma_filter(filters)

        results = self._collection.query(
            query_texts=[query],
            n_results=limit,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        candidates = []
        if results and results["ids"]:
            for i, cid in enumerate(results["ids"][0]):
                candidates.append({
                    "id": cid,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "relevance_score": round(
                        (1 - results["distances"][0][i]) * 100, 1
                    ) if results["distances"] else 0,
                    "document_preview": (
                        results["documents"][0][i][:200] + "..."
                        if results["documents"] and len(results["documents"][0][i]) > 200
                        else results["documents"][0][i] if results["documents"] else ""
                    ),
                })

        logger.info("候选人搜索完成", query=query, results_count=len(candidates))
        return candidates

    async def match_for_job(
        self,
        job_id: str,
        top_n: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        为指定职位匹配候选人

        Args:
            job_id: 职位 ID
            top_n: 返回的候选人数量

        Returns:
            匹配结果列表（含评分和理由）
        """
        # 1. 获取职位信息
        job_info = await self._get_job_info(job_id)
        if not job_info:
            raise ValueError(f"职位不存在：{job_id}")

        # 2. 向量搜索候选人
        search_query = f"{job_info['title']} {job_info.get('description', '')}"
        candidates = await self.search(search_query, limit=top_n * 2)

        # 3. LLM 精细评估 Top 候选人
        from app.agents.hr_agent import get_llm
        llm = get_llm()

        matched_results = []
        for candidate in candidates[:top_n]:
            try:
                evaluation = await self._evaluate_match(
                    llm, job_info, candidate
                )
                matched_results.append({
                    **candidate,
                    **evaluation,
                })
            except Exception as e:
                logger.warning(
                    "候选人评估失败",
                    candidate_id=candidate["id"],
                    error=str(e),
                )

        # 4. 按综合评分排序
        matched_results.sort(key=lambda x: x.get("overall_score", 0), reverse=True)

        logger.info(
            "职位匹配完成",
            job_id=job_id,
            matched_count=len(matched_results),
        )
        return matched_results

    async def _evaluate_match(
        self, llm, job_info: Dict, candidate: Dict
    ) -> Dict[str, Any]:
        """使用 LLM 评估单个候选人与职位的匹配度"""
        prompt = MATCH_EVALUATION_PROMPT.format(
            job_description=json.dumps(job_info, ensure_ascii=False),
            candidate_info=json.dumps(candidate, ensure_ascii=False),
        )
        response = await llm.ainvoke([HumanMessage(content=prompt)])

        content = response.content
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0].strip()
        else:
            json_str = content.strip()

        return json.loads(json_str)

    async def _get_job_info(self, job_id: str) -> Optional[Dict[str, Any]]:
        """获取职位信息（从数据库）"""
        # TODO: 从数据库读取职位信息
        # 临时占位实现
        return {
            "id": job_id,
            "title": "待实现",
            "description": "待实现",
        }

    def _build_chroma_filter(self, filters: Dict[str, Any]) -> Dict:
        """构建 ChromaDB 过滤条件"""
        conditions = []
        for key, value in filters.items():
            if isinstance(value, list):
                conditions.append({key: {"$in": value}})
            elif isinstance(value, dict):
                conditions.append({key: value})
            else:
                conditions.append({key: {"$eq": value}})

        if len(conditions) == 1:
            return conditions[0]
        return {"$and": conditions}
```

### 3.9 memory_service.py — OpenClaw 记忆集成

```python
"""
OpenClaw 记忆服务 — 管理 Agent 的长期记忆
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import structlog

from app.config import settings

logger = structlog.get_logger()

MEMORY_DB_PATH = ".openclaw/memory.db"


class MemoryService:
    """
    OpenClaw 记忆服务

    管理 HR Agent 的长期记忆，包括：
    - 用户偏好（HR 的筛选习惯、评分权重等）
    - 历史决策（哪些候选人被录用了、原因是什么）
    - 公司文化和用人标准
    - 常用的面试问题和模板
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or MEMORY_DB_PATH
        self._ensure_db()

    def _ensure_db(self):
        """确保数据库和表结构存在"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                metadata TEXT DEFAULT '{}',
                importance INTEGER DEFAULT 5,
                access_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NULL,
                UNIQUE(category, key)
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_memories_category
            ON memories(category)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_memories_importance
            ON memories(importance DESC)
        """)
        conn.commit()
        conn.close()

    def store(
        self,
        category: str,
        key: str,
        value: Any,
        metadata: Optional[Dict] = None,
        importance: int = 5,
        expires_at: Optional[datetime] = None,
    ):
        """
        存储记忆

        Args:
            category: 类别（preference / decision / culture / template）
            key: 键
            value: 值（自动序列化为 JSON）
            metadata: 额外元数据
            importance: 重要程度 1-10
            expires_at: 过期时间（可选）
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        value_str = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
        meta_str = json.dumps(metadata or {}, ensure_ascii=False)

        cursor.execute("""
            INSERT INTO memories (category, key, value, metadata, importance, expires_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(category, key)
            DO UPDATE SET
                value = excluded.value,
                metadata = excluded.metadata,
                importance = excluded.importance,
                expires_at = excluded.expires_at,
                updated_at = CURRENT_TIMESTAMP
        """, (category, key, value_str, meta_str, importance, expires_at))

        conn.commit()
        conn.close()
        logger.debug("记忆已存储", category=category, key=key)

    def recall(
        self,
        category: Optional[str] = None,
        key: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        回忆/检索记忆

        Args:
            category: 类别过滤
            key: 键过滤（支持模糊匹配）
            limit: 返回数量

        Returns:
            记忆列表
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = "SELECT * FROM memories WHERE 1=1"
        params = []

        # 过滤过期记忆
        query += " AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)"

        if category:
            query += " AND category = ?"
            params.append(category)
        if key:
            query += " AND key LIKE ?"
            params.append(f"%{key}%")

        query += " ORDER BY importance DESC, updated_at DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        # 更新访问计数
        for row in rows:
            cursor.execute(
                "UPDATE memories SET access_count = access_count + 1 WHERE id = ?",
                (row["id"],),
            )

        conn.commit()
        conn.close()

        return [
            {
                "category": row["category"],
                "key": row["key"],
                "value": json.loads(row["value"]) if row["value"].startswith(("{", "[")) else row["value"],
                "metadata": json.loads(row["metadata"]),
                "importance": row["importance"],
                "access_count": row["access_count"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
            for row in rows
        ]

    def forget(self, category: str, key: str):
        """删除特定记忆"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM memories WHERE category = ? AND key = ?",
            (category, key),
        )
        conn.commit()
        conn.close()
        logger.debug("记忆已删除", category=category, key=key)

    def get_context_summary(self, max_tokens: int = 2000) -> str:
        """
        生成记忆上下文摘要，用于注入到 Agent Prompt 中

        Args:
            max_tokens: 最大 Token 数（近似）

        Returns:
            记忆摘要文本
        """
        memories = self.recall(limit=100)
        if not memories:
            return "暂无历史记忆。"

        sections = {}
        for mem in memories:
            cat = mem["category"]
            if cat not in sections:
                sections[cat] = []
            sections[cat].append(f"- {mem['key']}: {mem['value']}")

        category_labels = {
            "preference": "用户偏好",
            "decision": "历史决策",
            "culture": "公司文化",
            "template": "常用模板",
        }

        summary_parts = []
        for cat, items in sections.items():
            label = category_labels.get(cat, cat)
            summary_parts.append(f"### {label}")
            summary_parts.extend(items[:10])  # 每个类别最多10条
            summary_parts.append("")

        summary = "\n".join(summary_parts)

        # 粗略截断
        if len(summary) > max_tokens * 3:
            summary = summary[: max_tokens * 3] + "\n...(更多记忆已省略)"

        return summary
```

---

## 4. 开发环境搭建步骤

### 4.1 Prerequisites

> [!warning] 开发环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Python | >= 3.11 | 推荐 3.12 |
| Node.js | >= 18 | 前端开发（可选） |
| Docker | >= 24.0 | 容器化部署 |
| Docker Compose | >= 2.20 | 多容器编排 |
| PostgreSQL | >= 16 | 业务数据库（Docker 提供） |
| Git | >= 2.40 | 版本控制 |

### 4.2 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/your-org/openclaw-hr-agent.git
cd openclaw-hr-agent

# 2. 创建 Python 虚拟环境
python3.12 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -e ".[dev]"
# 或使用 requirements.txt
pip install -r backend/requirements.txt

# 4. 复制环境变量配置
cp .env.example .env
# 编辑 .env 填入实际的 API Key 和配置

# 5. 启动基础设施（PostgreSQL + ChromaDB + Redis）
docker compose up -d db chromadb redis

# 6. 等待数据库就绪
sleep 5

# 7. 初始化数据库（运行迁移）
cd backend
alembic upgrade head

# 8. 导入种子数据（可选）
python scripts/seed_data.py
```

### 4.3 配置说明

> [!info] 关键配置项

**必须配置的环境变量**：
1. `ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY` — 至少配置一个 LLM API Key
2. `SECRET_KEY` — 应用密钥，用于 JWT 签名
3. `DATABASE_URL` — 数据库连接字符串

**可选配置**：
- 消息通道配置（企业微信/飞书）— 如需多平台集成
- SMTP 配置 — 如需邮件发送功能
- Redis 配置 — 如需缓存

### 4.4 本地运行

```bash
# 启动后端服务
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 服务启动后访问：
# API 文档：http://localhost:8000/docs
# 健康检查：http://localhost:8000/health
```

### 4.5 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_resume_parser.py -v

# 生成覆盖率报告
pytest --cov=app --cov-report=html

# 代码质量检查
ruff check app/
mypy app/
```

---

## 5. 部署方案

### 5.1 Docker 部署

> [!success] 推荐的部署方式

```bash
# 1. 构建并启动所有服务
docker compose up -d --build

# 2. 查看服务状态
docker compose ps

# 3. 查看日志
docker compose logs -f app

# 4. 初始化数据库
docker compose exec app alembic upgrade head

# 5. 健康检查
curl http://localhost:8000/health
```

**Dockerfile（后端）**：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    tesseract-ocr \
    tesseract-ocr-chi-sim \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建日志目录
RUN mkdir -p logs

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5.2 云服务器部署

> [!note] 生产环境部署建议

**推荐配置**：
- CPU: 4 核
- 内存: 8 GB
- 磁盘: 50 GB SSD
- 系统: Ubuntu 22.04 LTS

**部署步骤**：

```bash
# 1. 安装 Docker 和 Docker Compose
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 2. 克隆项目
git clone https://github.com/your-org/openclaw-hr-agent.git
cd openclaw-hr-agent

# 3. 配置环境变量
cp .env.example .env
vim .env  # 填入生产环境配置

# 4. 修改关键配置
# APP_ENV=production
# APP_DEBUG=false
# SECRET_KEY=<strong-random-key>
# DATABASE_URL=postgresql+asyncpg://...

# 5. 启动服务
docker compose -f docker-compose.yml up -d --build

# 6. 配置 Nginx 反向代理（可选）
sudo apt install nginx
# 配置 SSL 和反向代理...

# 7. 配置 systemd 服务（可选）
# 确保 Docker 容器随系统启动
```

### 5.3 与 OpenClaw Gateway 集成

> [!info] OpenClaw Gateway 集成

```bash
# 1. 安装 OpenClaw CLI
npm install -g @openclaw/cli

# 2. 初始化 OpenClaw 项目
openclaw init

# 3. 配置 Agent
# 编辑 .openclaw/openclaw.json（已在上方提供）

# 4. 注册自定义工具
openclaw tools register --config .openclaw/openclaw.json

# 5. 启动 OpenClaw Gateway
openclaw gateway start --port 8080

# 6. 测试 Agent 对话
openclaw chat "你好，我是HR，需要招聘一位后端工程师"

# 7. 连接消息通道
openclaw channel connect wechat_work
openclaw channel connect feishu
```

**集成架构说明**：

```
用户消息 → OpenClaw Gateway → Agent 编排引擎 → 调用后端 API → 返回结果
               ↓
         记忆系统读写
               ↓
         Skills 路由
               ↓
         工具调用（resume_parse / candidate_search / ...）
```

---

## 6. 相关笔记

> [!note] 项目相关文档链接

- [[docs/OpenClaw-HR-Agent-PRD|HR Agent PRD]] — 完整的产品需求文档
- [[docs/OpenClaw-视频攻略-赋范课堂28集|OpenClaw 视频攻略]] — OpenClaw 学习资料
- [[docs/OpenClaw 完整技术架构与应用详解|OpenClaw 完整技术架构与应用详解]] — OpenClaw 架构深度解析
- [[docs/OpenClaw-开发笔记-MiniOpenClaw与HR实战|OpenClaw 开发笔记]] — 开发实战笔记

---

#AI #OpenClaw #HR #工程设计 #Agent #项目结构
