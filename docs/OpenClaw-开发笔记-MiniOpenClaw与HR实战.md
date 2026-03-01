---
title: OpenClaw 开发笔记 — Mini OpenClaw 与 HR 数字员工实战
date: 2026-03-01
tags: [AI, OpenClaw, Agent, 开发笔记, LangChain, HR数字员工, 实战]
aliases:
  - Mini OpenClaw 开发笔记
  - HR数字员工实战
description: 基于赋范课堂 28 集 OpenClaw 教程，聚焦实战开发内容：构建 Mini OpenClaw 与 AI HR 数字员工
---

# OpenClaw 开发笔记 — Mini OpenClaw 与 HR 数字员工实战

> 创建日期: 2026-03-01
> 标签: #AI #OpenClaw #Agent #开发笔记 #LangChain #HR数字员工 #实战
> 相关笔记: [[docs/OpenClaw 完整技术架构与应用详解.md|OpenClaw 完整技术架构与应用详解]] | [[Research/OpenClaw-技术原理拆解-小白版.md|OpenClaw 技术原理拆解（小白版）]]

---

## 目录

1. [Part 1: Mini OpenClaw 技术栈规划](#part-1-mini-openclaw-技术栈规划)
2. [Part 2: 记忆系统实现](#part-2-记忆系统实现)
3. [Part 3: Skills 系统实现](#part-3-skills-系统实现)
4. [Part 4: 后端架构与代码](#part-4-后端架构与代码)
5. [Part 5: AI HR 数字员工开发](#part-5-ai-hr-数字员工开发)
6. [Part 6: 关键配置文件模板](#part-6-关键配置文件模板)

---

## Part 1: Mini OpenClaw 技术栈规划

> 对应赋范课堂 P8

### 1.1 为什么要做 Mini 版本

> [!question] 核心问题
> 原版 OpenClaw 是 TypeScript 项目，依赖 Node.js 生态，为什么不直接用原版？

做 Mini 版本有三个核心原因：

1. **国内环境适配**：原版 OpenClaw 大量依赖海外 API（Anthropic Claude、OpenAI 等），国内直连不稳定。Mini 版需要适配国产大模型（DeepSeek、通义千问、智谱 GLM 等），使用国内可访问的 embedding 服务。
2. **技术栈亲和度**：国内 AI 开发者主力语言是 Python，LangChain/LlamaIndex 等框架生态成熟。用 Python 重写能降低团队上手门槛，便于二次开发。
3. **功能裁剪聚焦**：原版支持 50+ Channel 和复杂的多 Agent 编排，但实际企业场景往往只需要单一接入渠道（如企业微信）+ 特定业务 Agent。Mini 版去掉冗余模块，聚焦核心能力。

### 1.2 核心技术选型

| 模块 | 原版 OpenClaw | Mini OpenClaw | 选型理由 |
|------|-------------|---------------|---------|
| 语言 | TypeScript / Node.js | **Python 3.11+** | 国内 AI 生态主力语言 |
| Agent 框架 | 自研运行时 | **LangChain 0.3+** | 社区成熟，工具链丰富 |
| 向量数据库 | SQLite + sqlite-vec | **ChromaDB / FAISS** | 开箱即用，部署简单 |
| 关系存储 | SQLite | **SQLite** | 保持一致，轻量可嵌入 |
| Web 框架 | 自研 WebSocket 服务 | **FastAPI** | 异步原生，自动文档 |
| 通信协议 | WebSocket (ws://127.0.0.1:18789) | **WebSocket + REST** | FastAPI 原生支持两者 |
| LLM 接入 | 自研 Provider 层 | **LangChain ChatModel** | 统一接口，切换模型一行代码 |
| 嵌入模型 | GGUF → OpenAI → Gemini 级联 | **sentence-transformers / 智谱 embedding** | 本地优先，国内可用 |
| 配置管理 | openclaw.json + TOML | **Pydantic Settings + YAML** | 类型安全，验证友好 |

### 1.3 与原版 OpenClaw 的对比

```
原版 OpenClaw                          Mini OpenClaw
┌─────────────────────┐                ┌─────────────────────┐
│ Channel 层 (50+)     │                │ Channel 层 (2-3个)   │
│ 全平台适配            │      →         │ 企微/飞书/Web        │
├─────────────────────┤                ├─────────────────────┤
│ Gateway 层           │                │ FastAPI 服务         │
│ 完整消息管线(6阶段)    │      →         │ 精简管线(4阶段)       │
│ 插件系统 + Cron       │                │ Skills 加载器        │
├─────────────────────┤                ├─────────────────────┤
│ LLM Provider 层      │                │ LangChain ChatModel │
│ 自研统一接口           │      →         │ 社区维护的适配器      │
└─────────────────────┘                └─────────────────────┘
```

> [!important] 关键取舍
> Mini 版保留了 OpenClaw 最核心的三个创新：**三层记忆系统**、**Skills 动态注入**、**工具沙箱执行**。去掉了 50+ Channel 适配、Lobster 工作流引擎、复杂的多 Agent 编排。

### 1.4 项目目录结构设计

```
mini-openclaw/
├── config/
│   ├── settings.yaml          # 主配置文件
│   ├── agents/
│   │   ├── AGENTS.md          # Agent 人设定义
│   │   └── SOUL.md            # Agent 灵魂设定
│   └── skills/
│       └── hr_recruitment/
│           └── SKILL.md       # HR 技能定义
├── src/
│   ├── __init__.py
│   ├── main.py                # FastAPI 入口
│   ├── core/
│   │   ├── __init__.py
│   │   ├── agent.py           # Agent 运行时
│   │   ├── config.py          # Pydantic 配置模型
│   │   └── pipeline.py        # 消息管线
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── manager.py         # 记忆管理器
│   │   ├── persistent.py      # 持久记忆 (MEMORY.md)
│   │   ├── temporal.py        # 时序记忆 (daily logs)
│   │   ├── session.py         # 会话记忆
│   │   ├── chunker.py         # 文本分块
│   │   └── search.py          # 混合搜索
│   ├── skills/
│   │   ├── __init__.py
│   │   ├── loader.py          # Skills 加载器
│   │   └── registry.py        # Skills 注册表
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base.py            # 工具基类
│   │   ├── file_ops.py        # 文件操作
│   │   ├── web_search.py      # 网络搜索
│   │   └── sandbox.py         # 沙箱执行
│   ├── channels/
│   │   ├── __init__.py
│   │   ├── web.py             # Web 聊天界面
│   │   └── wecom.py           # 企业微信
│   └── hr/
│       ├── __init__.py
│       ├── resume_parser.py   # 简历解析
│       ├── evaluator.py       # 候选人评估
│       ├── interviewer.py     # 面试问题生成
│       └── talent_pool.py     # 人才库
├── data/
│   ├── memory/
│   │   ├── MEMORY.md          # 持久记忆文件
│   │   └── 2026-03-01.md      # 时序记忆
│   ├── sessions/              # 会话 JSONL 文件
│   └── chroma_db/             # ChromaDB 持久化
├── tests/
│   ├── test_memory.py
│   ├── test_skills.py
│   ├── test_tools.py
│   └── test_hr.py
├── requirements.txt
├── Dockerfile
└── README.md
```

> [!tip] 开发建议
> 先搭好 `core/` 和 `memory/` 模块，确保 Agent 能跑通一轮对话，再逐步接入 skills、tools 和 channels。不要一开始就铺太大。

---

## Part 2: 记忆系统实现

> 对应赋范课堂 P9, P12, P13, P15

> [!abstract] 本节摘要
> 记忆系统是 OpenClaw 的核心创新。本节实现三层记忆架构的 Python 版本，包含向量索引、混合搜索、上下文压缩前记忆刷写等关键机制。

### 2.1 三层记忆架构的 Python 实现

原版 OpenClaw 的记忆分为三层：

| 层级 | 存储形式 | 生命周期 | Mini 版实现 |
|------|---------|---------|------------|
| **Persistent（持久记忆）** | MEMORY.md | 永久 | Markdown 文件 + 向量索引 |
| **Temporal（时序记忆）** | memory/YYYY-MM-DD.md | 按天归档 | 每日 Markdown 日志 |
| **Session（会话记忆）** | sessions/*.jsonl | 单次会话 | JSONL + 滑动窗口 |

#### 记忆管理器核心类

```python
"""memory/manager.py — 三层记忆管理器"""

import os
import json
from datetime import datetime, date
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field

from .persistent import PersistentMemory
from .temporal import TemporalMemory
from .session import SessionMemory
from .search import HybridSearchEngine


@dataclass
class MemoryConfig:
    """记忆系统配置"""
    base_dir: str = "./data/memory"
    chunk_size: int = 400          # 与原版一致：~400 tokens
    chunk_overlap: int = 80        # 与原版一致：80 token overlap
    vector_weight: float = 0.7     # 向量搜索权重
    bm25_weight: float = 0.3      # BM25 搜索权重
    mmr_lambda: float = 0.7       # MMR 多样性参数
    temporal_decay_half_life: int = 30  # 时间衰减半衰期（天）
    context_flush_threshold: float = 0.8  # 上下文 80% 阈值触发刷写
    max_context_tokens: int = 128000  # 最大上下文窗口


class MemoryManager:
    """
    三层记忆管理器 — Mini OpenClaw 核心组件

    职责：
    1. 管理持久/时序/会话三层记忆的读写
    2. 在上下文窗口达到 80% 时触发压缩前刷写
    3. 提供统一的混合搜索接口
    """

    def __init__(self, config: Optional[MemoryConfig] = None):
        self.config = config or MemoryConfig()
        self.base_dir = Path(self.config.base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # 初始化三层记忆
        self.persistent = PersistentMemory(
            filepath=self.base_dir / "MEMORY.md"
        )
        self.temporal = TemporalMemory(
            directory=self.base_dir
        )
        self.session = SessionMemory(
            directory=self.base_dir / "sessions"
        )

        # 初始化混合搜索引擎
        self.search_engine = HybridSearchEngine(
            vector_weight=self.config.vector_weight,
            bm25_weight=self.config.bm25_weight,
            mmr_lambda=self.config.mmr_lambda,
            decay_half_life=self.config.temporal_decay_half_life,
        )

        # 当前上下文 token 计数
        self._current_context_tokens = 0

    async def add_message(self, role: str, content: str,
                          session_id: str, metadata: dict = None):
        """添加一条消息到记忆系统"""
        timestamp = datetime.now().isoformat()
        message = {
            "role": role,
            "content": content,
            "timestamp": timestamp,
            "metadata": metadata or {},
        }

        # 1. 写入会话记忆
        self.session.append(session_id, message)

        # 2. 写入时序记忆
        today = date.today().isoformat()
        self.temporal.append(today, role, content)

        # 3. 更新向量索引
        await self.search_engine.index_message(content, {
            "role": role,
            "session_id": session_id,
            "timestamp": timestamp,
        })

        # 4. 检查是否需要压缩前刷写
        self._current_context_tokens += self._estimate_tokens(content)
        if self._should_flush():
            await self._flush_to_persistent(session_id)

    async def recall(self, query: str, top_k: int = 5) -> list[dict]:
        """
        混合搜索召回相关记忆

        搜索策略：0.7 * 向量余弦相似度 + 0.3 * BM25
        后处理：MMR 重排序 + 时间衰减
        """
        results = await self.search_engine.hybrid_search(
            query=query,
            top_k=top_k,
        )
        return results

    def get_session_context(self, session_id: str,
                            max_messages: int = 50) -> list[dict]:
        """获取当前会话的上下文（最近 N 条消息）"""
        return self.session.get_recent(session_id, max_messages)

    def _should_flush(self) -> bool:
        """判断是否达到 80% 上下文阈值"""
        threshold = self.config.max_context_tokens * \
            self.config.context_flush_threshold
        return self._current_context_tokens >= threshold

    async def _flush_to_persistent(self, session_id: str):
        """
        压缩前记忆刷写 — OpenClaw 的关键创新

        当上下文窗口使用达到 80% 时：
        1. 提取当前会话的关键信息
        2. 压缩写入 MEMORY.md
        3. 清理会话中的旧消息
        4. 重置 token 计数
        """
        # 获取当前会话所有消息
        messages = self.session.get_all(session_id)
        if not messages:
            return

        # 提取关键信息（通过 LLM 摘要）
        summary = await self._summarize_for_persistence(messages)

        # 追加到持久记忆
        self.persistent.append_section(
            title=f"会话摘要 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            content=summary,
        )

        # 保留最近 10 条消息，清理其余
        self.session.truncate(session_id, keep_recent=10)

        # 重置 token 计数（保留的消息大约占用的 tokens）
        recent = self.session.get_all(session_id)
        self._current_context_tokens = sum(
            self._estimate_tokens(m["content"]) for m in recent
        )

    async def _summarize_for_persistence(self, messages: list[dict]) -> str:
        """使用 LLM 将会话消息压缩为持久记忆摘要"""
        # 实际实现中调用 LLM 做摘要
        # 这里用占位逻辑
        conversation = "\n".join(
            f"{m['role']}: {m['content']}" for m in messages
        )
        # TODO: 调用 LangChain LLM 生成摘要
        return f"[待实现 LLM 摘要]\n{conversation[:500]}..."

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """粗略估算 token 数（中文约 1.5 字符/token）"""
        return int(len(text) / 1.5)
```

### 2.2 向量索引实现

> [!info] 嵌入模型选择
> 原版 OpenClaw 的嵌入模型优先级：本地 GGUF → OpenAI → Gemini → Voyage → Mistral。
> Mini 版推荐：**本地 sentence-transformers** → 智谱 embedding → OpenAI。本地模型推荐 `BAAI/bge-large-zh-v1.5`（中文效果好）。

#### 文本分块函数

```python
"""memory/chunker.py — 文本分块器"""

from dataclasses import dataclass
from typing import Generator


@dataclass
class Chunk:
    """文本块"""
    text: str
    index: int
    start_char: int
    end_char: int
    metadata: dict = None


def chunk_text(
    text: str,
    chunk_size: int = 400,
    chunk_overlap: int = 80,
    separator: str = "\n\n",
) -> list[Chunk]:
    """
    将文本分块，参数与原版 OpenClaw 保持一致。

    原版参数：
    - chunk_size: ~400 tokens
    - chunk_overlap: 80 tokens
    - 优先按段落分割，段落内按句子分割

    Args:
        text: 待分块文本
        chunk_size: 每块目标大小（字符数，约等于 token 数 * 1.5）
        chunk_overlap: 块间重叠字符数
        separator: 首选分割符

    Returns:
        Chunk 列表
    """
    # 将 token 数换算为字符数（中文约 1.5 字符/token）
    char_size = int(chunk_size * 1.5)
    char_overlap = int(chunk_overlap * 1.5)

    chunks = []
    # 第一级分割：按段落
    paragraphs = text.split(separator)

    current_chunk = ""
    current_start = 0
    char_pos = 0

    for para in paragraphs:
        if len(current_chunk) + len(para) + len(separator) <= char_size:
            current_chunk += (separator if current_chunk else "") + para
        else:
            if current_chunk:
                chunks.append(Chunk(
                    text=current_chunk.strip(),
                    index=len(chunks),
                    start_char=current_start,
                    end_char=current_start + len(current_chunk),
                ))
                # 保留 overlap 部分
                overlap_text = current_chunk[-char_overlap:] \
                    if len(current_chunk) > char_overlap else current_chunk
                current_start += len(current_chunk) - len(overlap_text)
                current_chunk = overlap_text + separator + para
            else:
                # 单个段落超长，按句子二次分割
                sentences = _split_sentences(para)
                for sent in sentences:
                    if len(current_chunk) + len(sent) <= char_size:
                        current_chunk += sent
                    else:
                        if current_chunk:
                            chunks.append(Chunk(
                                text=current_chunk.strip(),
                                index=len(chunks),
                                start_char=current_start,
                                end_char=current_start + len(current_chunk),
                            ))
                            overlap_text = current_chunk[-char_overlap:]
                            current_start += len(current_chunk) - len(overlap_text)
                            current_chunk = overlap_text + sent
                        else:
                            current_chunk = sent

    # 处理最后一个 chunk
    if current_chunk.strip():
        chunks.append(Chunk(
            text=current_chunk.strip(),
            index=len(chunks),
            start_char=current_start,
            end_char=current_start + len(current_chunk),
        ))

    return chunks


def _split_sentences(text: str) -> list[str]:
    """按句子分割（支持中英文标点）"""
    import re
    # 匹配中文句号、问号、感叹号、英文句号等
    sentences = re.split(r'(?<=[。！？.!?])\s*', text)
    return [s for s in sentences if s.strip()]
```

### 2.3 混合搜索实现

> [!warning] 搜索权重配置
> 原版 OpenClaw 使用 `0.7 x vector cosine + 0.3 x BM25` 的混合搜索，再用 MMR（lambda=0.7）重排序，加上时间衰减（halfLife=30天）。这组参数是经过大量实验调优的，Mini 版建议保持一致。

```python
"""memory/search.py — 混合搜索引擎"""

import math
import numpy as np
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

import chromadb
from rank_bm25 import BM25Okapi
import jieba


@dataclass
class SearchResult:
    """搜索结果"""
    text: str
    score: float
    metadata: dict
    source: str  # "vector" | "bm25" | "hybrid"


class HybridSearchEngine:
    """
    混合搜索引擎

    搜索公式：score = 0.7 * vector_cosine + 0.3 * bm25_score
    后处理：MMR 重排序 + 时间衰减

    对应原版 OpenClaw 的 sqlite-vec + BM25 实现
    """

    def __init__(
        self,
        vector_weight: float = 0.7,
        bm25_weight: float = 0.3,
        mmr_lambda: float = 0.7,
        decay_half_life: int = 30,
        collection_name: str = "memory",
        persist_dir: str = "./data/chroma_db",
    ):
        self.vector_weight = vector_weight
        self.bm25_weight = bm25_weight
        self.mmr_lambda = mmr_lambda
        self.decay_half_life = decay_half_life

        # 初始化 ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

        # BM25 索引（内存中维护）
        self._bm25_corpus: list[dict] = []
        self._bm25_index: Optional[BM25Okapi] = None
        self._rebuild_bm25()

    async def index_message(self, text: str, metadata: dict):
        """索引一条消息到向量库和 BM25"""
        doc_id = f"msg_{datetime.now().timestamp()}"

        # 写入 ChromaDB（自动生成 embedding）
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id],
        )

        # 更新 BM25 索引
        self._bm25_corpus.append({
            "id": doc_id,
            "text": text,
            "metadata": metadata,
        })
        self._rebuild_bm25()

    async def hybrid_search(
        self, query: str, top_k: int = 5
    ) -> list[SearchResult]:
        """
        执行混合搜索

        步骤：
        1. 向量搜索（ChromaDB cosine similarity）
        2. BM25 关键词搜索
        3. 分数融合：0.7 * vector + 0.3 * bm25
        4. 时间衰减加权
        5. MMR 重排序去重
        """
        if self.collection.count() == 0:
            return []

        # — 第一步：向量搜索 —
        vector_results = self.collection.query(
            query_texts=[query],
            n_results=min(top_k * 3, self.collection.count()),
        )

        vector_scores = {}
        vector_docs = {}
        if vector_results["ids"] and vector_results["ids"][0]:
            for i, doc_id in enumerate(vector_results["ids"][0]):
                # ChromaDB 返回的 distance 越小越相似，转为相似度
                distance = vector_results["distances"][0][i]
                similarity = 1 - distance  # cosine distance → similarity
                vector_scores[doc_id] = similarity
                vector_docs[doc_id] = {
                    "text": vector_results["documents"][0][i],
                    "metadata": vector_results["metadatas"][0][i],
                }

        # — 第二步：BM25 搜索 —
        bm25_scores = {}
        if self._bm25_index and self._bm25_corpus:
            query_tokens = list(jieba.cut(query))
            raw_scores = self._bm25_index.get_scores(query_tokens)

            # 归一化 BM25 分数到 [0, 1]
            max_score = max(raw_scores) if max(raw_scores) > 0 else 1
            for idx, score in enumerate(raw_scores):
                doc_id = self._bm25_corpus[idx]["id"]
                bm25_scores[doc_id] = score / max_score

        # — 第三步：分数融合 —
        all_doc_ids = set(vector_scores.keys()) | set(bm25_scores.keys())
        fused_results = []

        for doc_id in all_doc_ids:
            v_score = vector_scores.get(doc_id, 0.0)
            b_score = bm25_scores.get(doc_id, 0.0)
            fused_score = (
                self.vector_weight * v_score +
                self.bm25_weight * b_score
            )

            # 获取文档信息
            if doc_id in vector_docs:
                doc_info = vector_docs[doc_id]
            else:
                # 从 BM25 语料库中查找
                doc_info = next(
                    (d for d in self._bm25_corpus if d["id"] == doc_id),
                    {"text": "", "metadata": {}},
                )

            # — 第四步：时间衰减 —
            timestamp_str = doc_info.get("metadata", {}).get("timestamp", "")
            if timestamp_str:
                try:
                    doc_time = datetime.fromisoformat(timestamp_str)
                    days_ago = (datetime.now() - doc_time).days
                    decay = math.pow(0.5, days_ago / self.decay_half_life)
                    fused_score *= decay
                except (ValueError, TypeError):
                    pass

            fused_results.append(SearchResult(
                text=doc_info.get("text", doc_info.get("text", "")),
                score=fused_score,
                metadata=doc_info.get("metadata", {}),
                source="hybrid",
            ))

        # 按融合分数排序
        fused_results.sort(key=lambda x: x.score, reverse=True)

        # — 第五步：MMR 重排序 —
        final_results = self._mmr_rerank(
            fused_results, query, top_k
        )

        return final_results

    def _mmr_rerank(
        self,
        candidates: list[SearchResult],
        query: str,
        top_k: int,
    ) -> list[SearchResult]:
        """
        MMR (Maximal Marginal Relevance) 重排序

        公式：MMR = lambda * Sim(d, q) - (1 - lambda) * max(Sim(d, d_selected))
        lambda = 0.7 → 偏重相关性，同时保持一定多样性
        """
        if len(candidates) <= top_k:
            return candidates

        selected = []
        remaining = list(candidates)

        # 选第一个（最高分）
        selected.append(remaining.pop(0))

        while len(selected) < top_k and remaining:
            best_mmr_score = -float("inf")
            best_idx = 0

            for i, candidate in enumerate(remaining):
                # 相关性分数（已经是融合分数）
                relevance = candidate.score

                # 与已选文档的最大相似度（用简单的文本重叠度近似）
                max_sim_to_selected = max(
                    self._text_similarity(candidate.text, s.text)
                    for s in selected
                )

                # MMR 公式
                mmr_score = (
                    self.mmr_lambda * relevance -
                    (1 - self.mmr_lambda) * max_sim_to_selected
                )

                if mmr_score > best_mmr_score:
                    best_mmr_score = mmr_score
                    best_idx = i

            selected.append(remaining.pop(best_idx))

        return selected

    @staticmethod
    def _text_similarity(text1: str, text2: str) -> float:
        """简单的 Jaccard 文本相似度"""
        words1 = set(jieba.cut(text1))
        words2 = set(jieba.cut(text2))
        if not words1 or not words2:
            return 0.0
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union)

    def _rebuild_bm25(self):
        """重建 BM25 索引"""
        if not self._bm25_corpus:
            self._bm25_index = None
            return
        tokenized = [
            list(jieba.cut(doc["text"]))
            for doc in self._bm25_corpus
        ]
        self._bm25_index = BM25Okapi(tokenized)
```

### 2.4 上下文窗口管理与压缩前刷写

> [!important] 核心创新：80% 阈值刷写
> 这是 OpenClaw 记忆系统最关键的设计。当上下文使用量达到 `max_context_tokens * 0.8` 时，**在压缩上下文之前**先将重要信息刷写到持久记忆（MEMORY.md）。这确保了信息不会在上下文压缩时丢失。

```python
"""memory/persistent.py — 持久记忆管理"""

from pathlib import Path
from datetime import datetime


class PersistentMemory:
    """
    持久记忆层 — 对应 OpenClaw 的 MEMORY.md

    MEMORY.md 是 Agent 的"长期记忆本"，存储用户偏好、
    重要决策、项目上下文等需要永久保留的信息。
    """

    def __init__(self, filepath: Path):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            self._initialize()

    def _initialize(self):
        """初始化 MEMORY.md 文件"""
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        header = """# Auto Memory

## 用户偏好

## 项目上下文

## 重要决策记录

## 会话摘要归档
"""
        self.filepath.write_text(header, encoding="utf-8")

    def read(self) -> str:
        """读取全部持久记忆"""
        return self.filepath.read_text(encoding="utf-8")

    def append_section(self, title: str, content: str):
        """追加一个新的记忆段落"""
        current = self.read()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_section = f"\n### {title}\n> 记录时间: {timestamp}\n\n{content}\n"
        updated = current + new_section
        self.filepath.write_text(updated, encoding="utf-8")

    def update_preference(self, key: str, value: str):
        """更新用户偏好"""
        current = self.read()
        pref_line = f"- **{key}**: {value}"

        if f"**{key}**" in current:
            # 替换已有偏好
            import re
            pattern = rf"- \*\*{re.escape(key)}\*\*:.*"
            current = re.sub(pattern, pref_line, current)
        else:
            # 在"用户偏好"段落下追加
            current = current.replace(
                "## 用户偏好\n",
                f"## 用户偏好\n{pref_line}\n",
            )

        self.filepath.write_text(current, encoding="utf-8")
```

```python
"""memory/session.py — 会话记忆管理"""

import json
from pathlib import Path
from datetime import datetime


class SessionMemory:
    """
    会话记忆层 — 对应 OpenClaw 的 sessions/*.jsonl

    每个会话一个 JSONL 文件，每行一条消息记录。
    支持滑动窗口截断。
    """

    def __init__(self, directory: Path):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _session_file(self, session_id: str) -> Path:
        return self.directory / f"{session_id}.jsonl"

    def append(self, session_id: str, message: dict):
        """追加一条消息到会话文件"""
        filepath = self._session_file(session_id)
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(message, ensure_ascii=False) + "\n")

    def get_recent(self, session_id: str, n: int = 50) -> list[dict]:
        """获取最近 N 条消息"""
        all_msgs = self.get_all(session_id)
        return all_msgs[-n:]

    def get_all(self, session_id: str) -> list[dict]:
        """获取会话全部消息"""
        filepath = self._session_file(session_id)
        if not filepath.exists():
            return []
        messages = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    messages.append(json.loads(line))
        return messages

    def truncate(self, session_id: str, keep_recent: int = 10):
        """截断会话，只保留最近 N 条消息"""
        messages = self.get_all(session_id)
        recent = messages[-keep_recent:]
        filepath = self._session_file(session_id)
        with open(filepath, "w", encoding="utf-8") as f:
            for msg in recent:
                f.write(json.dumps(msg, ensure_ascii=False) + "\n")
```

### 2.5 对话记忆管理系统完整设计

```python
"""memory/temporal.py — 时序记忆管理"""

from pathlib import Path
from datetime import date, datetime


class TemporalMemory:
    """
    时序记忆层 — 对应 OpenClaw 的 memory/YYYY-MM-DD.md

    每天一个 Markdown 文件，自动归档当日对话摘要。
    用于回溯"某天聊过什么"。
    """

    def __init__(self, directory: Path):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _daily_file(self, day: str) -> Path:
        return self.directory / f"{day}.md"

    def append(self, day: str, role: str, content: str):
        """追加一条记录到当天的时序文件"""
        filepath = self._daily_file(day)
        timestamp = datetime.now().strftime("%H:%M:%S")

        if not filepath.exists():
            header = f"# 时序记忆 — {day}\n\n"
            filepath.write_text(header, encoding="utf-8")

        with open(filepath, "a", encoding="utf-8") as f:
            # 截断长内容，只记摘要
            summary = content[:200] + "..." if len(content) > 200 else content
            f.write(f"- **[{timestamp}] {role}**: {summary}\n")

    def get_day(self, day: str) -> str:
        """读取某天的全部记录"""
        filepath = self._daily_file(day)
        if not filepath.exists():
            return ""
        return filepath.read_text(encoding="utf-8")

    def get_recent_days(self, n: int = 7) -> list[tuple[str, str]]:
        """获取最近 N 天的记录"""
        files = sorted(self.directory.glob("????-??-??.md"), reverse=True)
        results = []
        for f in files[:n]:
            day = f.stem
            content = f.read_text(encoding="utf-8")
            results.append((day, content))
        return results
```

> [!tip] 记忆系统调试技巧
> 在开发阶段，可以把 `context_flush_threshold` 设为 0.3（30%），这样更容易触发刷写逻辑来测试。上线前记得改回 0.8。

---

## Part 3: Skills 系统实现

> 对应赋范课堂 P10, P14

> [!abstract] 本节摘要
> Skills 是 OpenClaw 的"即插即用能力模块"。一个 SKILL.md 文件就是一个技能，用 YAML frontmatter 描述元信息，用自然语言描述指令，通过 Gate 规则控制何时激活。

### 3.1 SKILL.md 格式定义

每个 Skill 是一个 Markdown 文件，格式如下：

```markdown
---
name: hr_recruitment
display_name: HR 招聘助手
description: 协助完成简历筛选、候选人评估、面试问题生成等 HR 招聘相关任务
version: 1.0.0
author: mini-openclaw
tags: [hr, recruitment, 招聘, 面试]
gate:
  - type: keyword
    keywords: [简历, 招聘, 候选人, 面试, HR, 人才]
  - type: intent
    intents: [screen_resume, evaluate_candidate, generate_questions]
tools:
  - file_read
  - file_write
  - web_search
priority: 10
---

# HR 招聘助手技能

## 指令

你是一位专业的 HR 招聘助手。当用户提出与招聘相关的需求时，你应当：

1. **简历筛选**：根据岗位 JD 要求，分析简历中的关键信息，给出匹配度评分
2. **候选人评估**：从技术能力、文化匹配度、成长潜力三个维度评估候选人
3. **面试问题生成**：根据岗位要求和候选人背景，生成有针对性的面试题
4. **邮件起草**：起草面试邀请、offer、拒信等招聘相关邮件

## 输出格式

- 简历筛选结果用表格呈现
- 评估报告用结构化的 Markdown 格式
- 面试问题按难度分级（基础/进阶/深入）

## 注意事项

- 保持客观公正，避免任何形式的偏见
- 遵守劳动法相关规定
- 保护候选人隐私信息
```

### 3.2 Skills 加载器实现

```python
"""skills/loader.py — Skills 加载器"""

import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GateRule:
    """Gate 规则 — 控制 Skill 何时被激活"""
    type: str             # "keyword" | "intent" | "always" | "manual"
    keywords: list[str] = field(default_factory=list)
    intents: list[str] = field(default_factory=list)

    def matches(self, user_input: str, detected_intent: str = "") -> bool:
        """判断用户输入是否匹配此 Gate 规则"""
        if self.type == "always":
            return True
        if self.type == "manual":
            return False  # 需要显式调用
        if self.type == "keyword":
            return any(kw in user_input for kw in self.keywords)
        if self.type == "intent":
            return detected_intent in self.intents
        return False


@dataclass
class Skill:
    """一个 Skill 的完整定义"""
    name: str
    display_name: str
    description: str
    version: str
    author: str
    tags: list[str]
    gates: list[GateRule]
    tools: list[str]
    priority: int
    instructions: str       # Markdown 正文部分（自然语言指令）
    source_path: str        # SKILL.md 文件路径


class SkillLoader:
    """
    Skills 加载器

    职责：
    1. 扫描 skills 目录，加载所有 SKILL.md 文件
    2. 解析 YAML frontmatter 和 Markdown 正文
    3. 根据 Gate 规则判断哪些 Skills 应被激活
    4. 将激活的 Skills 注入 Agent prompt
    """

    def __init__(self, skills_dir: str = "./config/skills"):
        self.skills_dir = Path(skills_dir)
        self.skills: dict[str, Skill] = {}
        self._load_all()

    def _load_all(self):
        """扫描并加载所有 SKILL.md 文件"""
        if not self.skills_dir.exists():
            return

        for skill_file in self.skills_dir.rglob("SKILL.md"):
            try:
                skill = self._parse_skill_file(skill_file)
                self.skills[skill.name] = skill
            except Exception as e:
                print(f"[SkillLoader] 加载失败: {skill_file} — {e}")

    def _parse_skill_file(self, filepath: Path) -> Skill:
        """解析单个 SKILL.md 文件"""
        content = filepath.read_text(encoding="utf-8")

        # 分离 YAML frontmatter 和 Markdown 正文
        frontmatter, body = self._split_frontmatter(content)

        # 解析 YAML
        meta = yaml.safe_load(frontmatter)

        # 解析 Gate 规则
        gates = []
        for gate_def in meta.get("gate", []):
            gates.append(GateRule(
                type=gate_def.get("type", "keyword"),
                keywords=gate_def.get("keywords", []),
                intents=gate_def.get("intents", []),
            ))

        return Skill(
            name=meta.get("name", filepath.parent.name),
            display_name=meta.get("display_name", meta.get("name", "")),
            description=meta.get("description", ""),
            version=meta.get("version", "1.0.0"),
            author=meta.get("author", "unknown"),
            tags=meta.get("tags", []),
            gates=gates,
            tools=meta.get("tools", []),
            priority=meta.get("priority", 0),
            instructions=body.strip(),
            source_path=str(filepath),
        )

    @staticmethod
    def _split_frontmatter(content: str) -> tuple[str, str]:
        """
        分离 YAML frontmatter 和 Markdown 正文

        格式：
        ---
        yaml content
        ---
        markdown body
        """
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return "", content

    def get_active_skills(
        self,
        user_input: str,
        detected_intent: str = "",
    ) -> list[Skill]:
        """
        根据用户输入和检测到的意图，返回应激活的 Skills。
        按 priority 降序排列。
        """
        active = []
        for skill in self.skills.values():
            for gate in skill.gates:
                if gate.matches(user_input, detected_intent):
                    active.append(skill)
                    break  # 一个 gate 匹配即可

        # 按优先级降序排列
        active.sort(key=lambda s: s.priority, reverse=True)
        return active

    def get_skill_by_name(self, name: str) -> Optional[Skill]:
        """按名称获取 Skill"""
        return self.skills.get(name)

    def list_skills(self) -> list[dict]:
        """列出所有已加载的 Skills（用于调试/管理界面）"""
        return [
            {
                "name": s.name,
                "display_name": s.display_name,
                "description": s.description,
                "tags": s.tags,
                "priority": s.priority,
            }
            for s in self.skills.values()
        ]
```

### 3.3 动态注入到 Agent Prompt

> [!important] Skill 注入时机
> Skills 在每次用户发消息时动态判断是否注入。这不是一次性加载，而是**每轮对话都重新评估**。这样 Agent 的 system prompt 能根据对话内容动态变化。

```python
"""skills/registry.py — Skills 注册表与 Prompt 注入"""

from .loader import SkillLoader, Skill


class SkillRegistry:
    """
    Skills 注册表

    管理 Skills 的生命周期，负责将激活的 Skills 注入到 Agent 的 prompt 中。
    """

    def __init__(self, skills_dir: str = "./config/skills"):
        self.loader = SkillLoader(skills_dir)

    def inject_skills_to_prompt(
        self,
        base_system_prompt: str,
        user_input: str,
        detected_intent: str = "",
    ) -> str:
        """
        将激活的 Skills 指令注入到 system prompt 中。

        注入位置：在 base system prompt 之后追加。
        每个 Skill 的 instructions 作为独立段落插入。

        Args:
            base_system_prompt: 基础系统提示词
            user_input: 用户当前输入
            detected_intent: 检测到的用户意图

        Returns:
            增强后的 system prompt
        """
        active_skills = self.loader.get_active_skills(
            user_input, detected_intent
        )

        if not active_skills:
            return base_system_prompt

        # 构建 Skills 注入段落
        skills_section = "\n\n---\n\n## 已激活技能\n\n"
        for skill in active_skills:
            skills_section += f"### [{skill.display_name}] (v{skill.version})\n"
            skills_section += f"> {skill.description}\n\n"
            skills_section += skill.instructions
            skills_section += "\n\n"

        # 构建工具列表
        available_tools = set()
        for skill in active_skills:
            available_tools.update(skill.tools)

        if available_tools:
            skills_section += f"\n**可用工具**: {', '.join(sorted(available_tools))}\n"

        return base_system_prompt + skills_section

    def get_tools_for_active_skills(
        self,
        user_input: str,
        detected_intent: str = "",
    ) -> list[str]:
        """获取当前激活 Skills 所需的工具列表"""
        active_skills = self.loader.get_active_skills(
            user_input, detected_intent
        )
        tools = set()
        for skill in active_skills:
            tools.update(skill.tools)
        return sorted(tools)
```

---

## Part 4: 后端架构与代码

> 对应赋范课堂 P16, P17, P18

### 4.1 后端整体架构

```
┌──────────────────────────────────────────────────────┐
│                    FastAPI Application                │
│                                                      │
│  ┌─────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ REST API │  │WebSocket │  │ Static Files     │   │
│  │ /api/v1  │  │ /ws      │  │ /static (Web UI) │   │
│  └────┬─────┘  └────┬─────┘  └──────────────────┘   │
│       │              │                                │
│  ┌────▼──────────────▼────────────────────────────┐  │
│  │              Pipeline (消息管线)                  │  │
│  │  1. Ingestion → 2. Auth → 3. Context → 4. LLM  │  │
│  └────────────────────┬───────────────────────────┘  │
│                       │                               │
│  ┌────────────────────▼───────────────────────────┐  │
│  │              Core Services                      │  │
│  │  ┌──────────┐ ┌────────┐ ┌──────────────────┐ │  │
│  │  │ Memory   │ │ Skills │ │ Tool Executor    │ │  │
│  │  │ Manager  │ │Registry│ │ (Sandbox)        │ │  │
│  │  └──────────┘ └────────┘ └──────────────────┘ │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

> [!note] 精简管线
> 原版 OpenClaw 有六阶段消息管线（Ingestion → Access Control → Session Resolution → Context Assembly → Model Invocation → Response Delivery）。Mini 版合并为四阶段：Ingestion（接收归一化）→ Auth（认证鉴权）→ Context（上下文组装，含 Skills 注入 + 记忆召回）→ LLM（模型调用 + 响应投递）。

### 4.2 API 路由设计

```python
"""main.py — FastAPI 应用入口"""

import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.core.agent import AgentRuntime
from src.core.config import Settings
from src.memory.manager import MemoryManager, MemoryConfig
from src.skills.registry import SkillRegistry


# --- 应用初始化 ---

settings = Settings()
memory_manager: MemoryManager = None
skill_registry: SkillRegistry = None
agent_runtime: AgentRuntime = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    global memory_manager, skill_registry, agent_runtime

    # 启动时初始化
    memory_config = MemoryConfig(
        base_dir=settings.memory_dir,
        max_context_tokens=settings.max_context_tokens,
    )
    memory_manager = MemoryManager(config=memory_config)
    skill_registry = SkillRegistry(skills_dir=settings.skills_dir)
    agent_runtime = AgentRuntime(
        memory=memory_manager,
        skills=skill_registry,
        settings=settings,
    )
    print(f"[Mini OpenClaw] 启动完成，已加载 {len(skill_registry.loader.skills)} 个 Skills")

    yield

    # 关闭时清理
    print("[Mini OpenClaw] 正在关闭...")


app = FastAPI(
    title="Mini OpenClaw",
    description="轻量版 OpenClaw Agent 服务",
    version="0.1.0",
    lifespan=lifespan,
)


# --- 数据模型 ---

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    skills_used: list[str] = []
    tools_called: list[str] = []

class SkillInfo(BaseModel):
    name: str
    display_name: str
    description: str
    tags: list[str]

class HealthResponse(BaseModel):
    status: str
    version: str
    skills_loaded: int
    memory_status: str


# --- REST API 路由 ---

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查"""
    return HealthResponse(
        status="ok",
        version="0.1.0",
        skills_loaded=len(skill_registry.loader.skills),
        memory_status="active",
    )

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    同步聊天接口

    处理流程：
    1. 分配/复用 session_id
    2. 记忆系统记录用户消息
    3. Agent 运行时处理（Skills 注入 + 记忆召回 + LLM 调用）
    4. 记忆系统记录 Agent 回复
    5. 返回结果
    """
    session_id = request.session_id or str(uuid.uuid4())

    # 记录用户消息
    await memory_manager.add_message(
        role="user",
        content=request.message,
        session_id=session_id,
    )

    # Agent 处理
    result = await agent_runtime.process(
        user_input=request.message,
        session_id=session_id,
    )

    # 记录 Agent 回复
    await memory_manager.add_message(
        role="assistant",
        content=result["reply"],
        session_id=session_id,
    )

    return ChatResponse(
        reply=result["reply"],
        session_id=session_id,
        skills_used=result.get("skills_used", []),
        tools_called=result.get("tools_called", []),
    )

@app.get("/api/v1/skills", response_model=list[SkillInfo])
async def list_skills():
    """列出所有已加载的 Skills"""
    return skill_registry.loader.list_skills()

@app.get("/api/v1/memory/{session_id}")
async def get_session_memory(session_id: str, limit: int = 50):
    """获取会话记忆"""
    messages = memory_manager.get_session_context(session_id, limit)
    return {"session_id": session_id, "messages": messages}


# --- WebSocket 路由 ---

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket 实时聊天接口

    对应原版 OpenClaw 的 ws://127.0.0.1:18789
    Mini 版简化了协议，直接传输 JSON 消息。
    """
    await websocket.accept()
    try:
        while True:
            # 接收消息
            data = await websocket.receive_json()
            user_message = data.get("message", "")

            if not user_message:
                continue

            # 记录 + 处理
            await memory_manager.add_message(
                role="user",
                content=user_message,
                session_id=session_id,
            )

            # 流式响应（逐步发送 token）
            async for chunk in agent_runtime.process_stream(
                user_input=user_message,
                session_id=session_id,
            ):
                await websocket.send_json({
                    "type": "stream",
                    "content": chunk,
                })

            # 发送完成信号
            await websocket.send_json({
                "type": "done",
                "session_id": session_id,
            })

    except WebSocketDisconnect:
        print(f"[WS] 客户端断开: {session_id}")
```

### 4.3 配置管理

```python
"""core/config.py — 配置管理（Pydantic Settings）"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Mini OpenClaw 配置

    优先级（与原版 OpenClaw 的 API key 优先级理念一致）：
    环境变量 → .env 文件 → settings.yaml → 默认值
    """

    # --- 基础配置 ---
    app_name: str = "Mini OpenClaw"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    # --- LLM 配置 ---
    # 格式与原版一致: "provider/model"
    default_model: str = "deepseek/deepseek-chat"
    deepseek_api_key: str = ""
    openai_api_key: str = ""
    zhipu_api_key: str = ""

    # --- 嵌入模型配置 ---
    embedding_model: str = "BAAI/bge-large-zh-v1.5"
    embedding_device: str = "cpu"  # cpu | cuda | mps

    # --- 记忆系统配置 ---
    memory_dir: str = "./data/memory"
    max_context_tokens: int = 128000
    chunk_size: int = 400
    chunk_overlap: int = 80

    # --- Skills 配置 ---
    skills_dir: str = "./config/skills"

    # --- 安全配置 ---
    api_key: str = ""  # API 访问密钥
    sandbox_enabled: bool = True

    model_config = {
        "env_file": ".env",
        "env_prefix": "MINI_OPENCLAW_",
    }
```

### 4.4 需求文档模板

> [!tip] 开发规范
> 在正式开发前，先写好需求文档（PRD），再写 README。这是赋范课堂反复强调的工程实践。

需求文档应包含以下结构：

```markdown
# Mini OpenClaw — 需求文档（PRD）

## 1. 产品概述
- 一句话描述
- 目标用户
- 核心价值

## 2. 功能需求
### 2.1 P0 (必须实现)
- [ ] 单轮对话
- [ ] 三层记忆系统
- [ ] Skills 动态加载
### 2.2 P1 (应该实现)
- [ ] WebSocket 流式输出
- [ ] 企业微信接入
### 2.3 P2 (可以后续)
- [ ] 多 Agent 协作
- [ ] Cron 定时任务

## 3. 非功能需求
- 响应延迟 < 3s
- 支持并发 100 会话
- 记忆检索 < 500ms

## 4. 技术方案
（详见本文档各 Part）

## 5. 里程碑
- Week 1-2: 核心框架 + 记忆系统
- Week 3: Skills 系统 + 工具沙箱
- Week 4: HR Agent + 测试
```

---

## Part 5: AI HR 数字员工开发

> 对应赋范课堂 P19-P28

> [!abstract] 本节摘要
> HR 数字员工是 Mini OpenClaw 的第一个业务 Agent。它能完成简历筛选、候选人评估、面试问题生成、招聘邮件起草、人才库搜索等 HR 全流程任务。

### 5.1 HR Agent 需求分析

```
HR 数字员工功能矩阵
┌───────────────────┬──────────┬──────────────────────────┐
│ 功能模块           │ 优先级    │ 核心能力                  │
├───────────────────┼──────────┼──────────────────────────┤
│ 简历筛选           │ P0       │ 解析简历 + 匹配 JD        │
│ 候选人评估         │ P0       │ 多维度打分 + 综合评语      │
│ 面试问题生成       │ P0       │ 按岗位/经验定制问题        │
│ 招聘邮件起草       │ P1       │ 面邀/Offer/拒信模板        │
│ 人才库搜索         │ P1       │ 向量搜索历史候选人         │
│ 音频转文字         │ P2       │ 面试录音 → 文字记录        │
│ PDF 转 Markdown    │ P2       │ 简历 PDF → 结构化 MD       │
└───────────────────┴──────────┴──────────────────────────┘
```

### 5.2 人设(Persona)配置

#### AGENTS.md — HR Agent 版

```markdown
---
name: hr_agent
display_name: 小招 — AI 招聘助手
model: deepseek/deepseek-chat
temperature: 0.3
max_tokens: 4096
tools:
  - file_read
  - file_write
  - web_search
  - pdf_to_markdown
skills:
  - hr_recruitment
---

# Agent 配置：小招

## 角色定义
你是"小招"，一位专业、高效、细致的 AI 招聘助手。你服务于 HR 团队，帮助他们完成招聘全流程的各项任务。

## 工作原则
1. **客观公正**：评估候选人时基于事实和数据，不受性别、年龄、院校等无关因素影响
2. **保密合规**：严格保护候选人个人信息，遵守劳动法和数据保护法规
3. **高效精准**：用最少的交互完成任务，输出结构化、可操作的结果
4. **主动建议**：在完成指定任务的同时，主动给出专业建议和风险提示
```

#### SOUL.md — HR Agent 灵魂设定

```markdown
---
agent: hr_agent
type: soul
---

# 小招的灵魂

## 性格特征
- 专业严谨：对招聘流程和劳动法了如指掌
- 温和耐心：面对重复性工作保持高质量输出
- 细致入微：不遗漏简历中的任何关键信息
- 有同理心：理解候选人和面试官双方的感受

## 沟通风格
- 使用专业但不晦涩的语言
- 输出结构化清晰的报告
- 关键数据用表格呈现
- 重要判断给出理由

## 知识领域
- 招聘全流程管理
- 岗位 JD 分析
- 简历解析与评估
- 面试方法论（行为面试法 STAR、结构化面试）
- 劳动法基础知识
- 薪酬市场行情（辅助参考）
```

### 5.3 内置工具集成

```python
"""tools/base.py — 工具基类"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:
    """工具执行结果"""
    success: bool
    data: Any
    error: str = ""


class BaseTool(ABC):
    """
    工具基类

    对应原版 OpenClaw 的工具系统。
    原版有 8 组工具（runtime, fs, web, ui, messaging, sessions, memory, automation）。
    Mini 版精简为 4 组（fs, web, memory, hr）。
    """

    name: str
    description: str

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """执行工具"""
        pass

    def to_function_schema(self) -> dict:
        """转为 LLM function calling 的 JSON Schema"""
        raise NotImplementedError
```

```python
"""tools/file_ops.py — 文件操作工具"""

import os
from pathlib import Path

from .base import BaseTool, ToolResult


class FileReadTool(BaseTool):
    name = "file_read"
    description = "读取文件内容"

    async def execute(self, filepath: str) -> ToolResult:
        """读取指定文件"""
        try:
            path = Path(filepath)
            if not path.exists():
                return ToolResult(success=False, data=None,
                                  error=f"文件不存在: {filepath}")
            content = path.read_text(encoding="utf-8")
            return ToolResult(success=True, data=content)
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))

    def to_function_schema(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "要读取的文件路径",
                    },
                },
                "required": ["filepath"],
            },
        }


class FileWriteTool(BaseTool):
    name = "file_write"
    description = "写入内容到文件"

    async def execute(self, filepath: str, content: str) -> ToolResult:
        """写入文件"""
        try:
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return ToolResult(success=True,
                              data=f"已写入 {len(content)} 字符到 {filepath}")
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))

    def to_function_schema(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "目标文件路径",
                    },
                    "content": {
                        "type": "string",
                        "description": "要写入的内容",
                    },
                },
                "required": ["filepath", "content"],
            },
        }
```

### 5.4 HR 功能实现

#### 简历筛选

```python
"""hr/resume_parser.py — 简历解析与筛选"""

import re
from dataclasses import dataclass, field
from typing import Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


@dataclass
class ResumeProfile:
    """解析后的简历结构"""
    name: str = ""
    email: str = ""
    phone: str = ""
    education: list[dict] = field(default_factory=list)
    experience: list[dict] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    years_of_experience: float = 0.0
    summary: str = ""


@dataclass
class ScreeningResult:
    """筛选结果"""
    candidate_name: str
    overall_score: float          # 0-100
    skill_match: float            # 技能匹配度 0-100
    experience_match: float       # 经验匹配度 0-100
    education_match: float        # 学历匹配度 0-100
    recommendation: str           # "强烈推荐" | "推荐" | "待定" | "不推荐"
    highlights: list[str] = field(default_factory=list)   # 亮点
    concerns: list[str] = field(default_factory=list)     # 顾虑
    reasoning: str = ""           # 详细推理


class ResumeScreener:
    """
    简历筛选器

    使用 LLM 解析简历文本，与 JD 进行匹配打分。
    """

    PARSE_PROMPT = ChatPromptTemplate.from_messages([
        ("system", """你是一位专业的简历解析专家。请将以下简历文本解析为结构化的 JSON 格式。

输出 JSON 格式：
{{
    "name": "姓名",
    "email": "邮箱",
    "phone": "电话",
    "education": [{{"school": "学校", "degree": "学位", "major": "专业", "year": "毕业年份"}}],
    "experience": [{{"company": "公司", "title": "职位", "duration": "时长", "description": "职责描述"}}],
    "skills": ["技能1", "技能2"],
    "years_of_experience": 5.0,
    "summary": "一句话总结"
}}"""),
        ("user", "请解析以下简历：\n\n{resume_text}"),
    ])

    SCREENING_PROMPT = ChatPromptTemplate.from_messages([
        ("system", """你是一位资深 HR 招聘专家。请根据岗位 JD 和候选人简历，进行匹配度评估。

评估维度（各 0-100 分）：
1. **技能匹配度** (skill_match)：候选人技术栈与 JD 要求的吻合度
2. **经验匹配度** (experience_match)：工作年限和行业经验的匹配
3. **学历匹配度** (education_match)：学历背景是否满足要求

综合评分公式：overall = skill_match * 0.5 + experience_match * 0.35 + education_match * 0.15

推荐等级：
- >= 80: 强烈推荐
- >= 65: 推荐
- >= 50: 待定
- < 50: 不推荐

输出 JSON 格式：
{{
    "overall_score": 75.0,
    "skill_match": 80.0,
    "experience_match": 70.0,
    "education_match": 75.0,
    "recommendation": "推荐",
    "highlights": ["亮点1", "亮点2"],
    "concerns": ["顾虑1"],
    "reasoning": "详细推理说明"
}}"""),
        ("user", "岗位 JD：\n{jd_text}\n\n候选人简历：\n{resume_text}"),
    ])

    def __init__(self, llm):
        self.llm = llm
        self.json_parser = JsonOutputParser()

    async def parse_resume(self, resume_text: str) -> ResumeProfile:
        """将简历文本解析为结构化数据"""
        chain = self.PARSE_PROMPT | self.llm | self.json_parser
        result = await chain.ainvoke({"resume_text": resume_text})

        return ResumeProfile(
            name=result.get("name", ""),
            email=result.get("email", ""),
            phone=result.get("phone", ""),
            education=result.get("education", []),
            experience=result.get("experience", []),
            skills=result.get("skills", []),
            years_of_experience=result.get("years_of_experience", 0),
            summary=result.get("summary", ""),
        )

    async def screen_resume(
        self, resume_text: str, jd_text: str
    ) -> ScreeningResult:
        """根据 JD 筛选简历"""
        chain = self.SCREENING_PROMPT | self.llm | self.json_parser
        result = await chain.ainvoke({
            "resume_text": resume_text,
            "jd_text": jd_text,
        })

        return ScreeningResult(
            candidate_name=result.get("candidate_name", "未知"),
            overall_score=result.get("overall_score", 0),
            skill_match=result.get("skill_match", 0),
            experience_match=result.get("experience_match", 0),
            education_match=result.get("education_match", 0),
            recommendation=result.get("recommendation", "待定"),
            highlights=result.get("highlights", []),
            concerns=result.get("concerns", []),
            reasoning=result.get("reasoning", ""),
        )

    async def batch_screen(
        self, resumes: list[str], jd_text: str
    ) -> list[ScreeningResult]:
        """批量筛选简历"""
        import asyncio
        tasks = [
            self.screen_resume(resume, jd_text) for resume in resumes
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if isinstance(r, ScreeningResult)]
```

#### 候选人评估

```python
"""hr/evaluator.py — 候选人多维度评估"""

from dataclasses import dataclass, field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


@dataclass
class EvaluationReport:
    """评估报告"""
    candidate_name: str
    technical_score: float        # 技术能力 0-10
    cultural_fit: float           # 文化匹配 0-10
    growth_potential: float       # 成长潜力 0-10
    communication: float          # 沟通能力 0-10
    overall_rating: str           # A/B/C/D
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    interview_focus: list[str] = field(default_factory=list)
    salary_suggestion: str = ""
    summary: str = ""


class CandidateEvaluator:
    """
    候选人综合评估器

    从四个维度评估候选人：
    1. 技术能力：硬技能、项目经验、技术深度
    2. 文化匹配度：价值观、工作风格、团队协作
    3. 成长潜力：学习能力、职业规划、自驱力
    4. 沟通能力：表达清晰度、逻辑性、互动质量
    """

    EVAL_PROMPT = ChatPromptTemplate.from_messages([
        ("system", """你是一位资深的人才评估专家，擅长从多维度全面评估候选人。

请根据以下信息对候选人进行综合评估：

评估维度（各 0-10 分）：
1. 技术能力 (technical_score)
2. 文化匹配度 (cultural_fit)
3. 成长潜力 (growth_potential)
4. 沟通能力 (communication)

综合等级：
- A (优秀): 平均分 >= 8
- B (良好): 平均分 >= 6.5
- C (一般): 平均分 >= 5
- D (不合格): 平均分 < 5

输出 JSON：
{{
    "candidate_name": "姓名",
    "technical_score": 8.0,
    "cultural_fit": 7.5,
    "growth_potential": 8.5,
    "communication": 7.0,
    "overall_rating": "A",
    "strengths": ["优势1", "优势2"],
    "weaknesses": ["不足1"],
    "interview_focus": ["面试重点关注1", "面试重点关注2"],
    "salary_suggestion": "建议薪资范围",
    "summary": "综合评价"
}}"""),
        ("user", """候选人简历：
{resume}

岗位要求：
{jd}

公司文化描述：
{culture}

附加信息（如有）：
{additional_info}"""),
    ])

    def __init__(self, llm):
        self.llm = llm
        self.json_parser = JsonOutputParser()

    async def evaluate(
        self,
        resume: str,
        jd: str,
        culture: str = "开放、协作、追求卓越",
        additional_info: str = "无",
    ) -> EvaluationReport:
        """综合评估候选人"""
        chain = self.EVAL_PROMPT | self.llm | self.json_parser
        result = await chain.ainvoke({
            "resume": resume,
            "jd": jd,
            "culture": culture,
            "additional_info": additional_info,
        })

        return EvaluationReport(
            candidate_name=result.get("candidate_name", ""),
            technical_score=result.get("technical_score", 0),
            cultural_fit=result.get("cultural_fit", 0),
            growth_potential=result.get("growth_potential", 0),
            communication=result.get("communication", 0),
            overall_rating=result.get("overall_rating", "C"),
            strengths=result.get("strengths", []),
            weaknesses=result.get("weaknesses", []),
            interview_focus=result.get("interview_focus", []),
            salary_suggestion=result.get("salary_suggestion", ""),
            summary=result.get("summary", ""),
        )
```

#### 面试问题生成

```python
"""hr/interviewer.py — 面试问题生成器"""

from dataclasses import dataclass, field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


@dataclass
class InterviewQuestion:
    """面试问题"""
    question: str
    category: str          # "技术" | "行为" | "情景" | "开放"
    difficulty: str        # "基础" | "进阶" | "深入"
    evaluation_points: list[str] = field(default_factory=list)
    ideal_answer_hints: str = ""
    follow_up: str = ""    # 追问方向


class InterviewQuestionGenerator:
    """
    面试问题生成器

    支持多种面试方法论：
    - STAR 行为面试法（Situation-Task-Action-Result）
    - 结构化面试
    - 技术深度探测
    - 情景模拟
    """

    GENERATE_PROMPT = ChatPromptTemplate.from_messages([
        ("system", """你是一位面试官培训专家。请根据岗位要求和候选人背景，生成有针对性的面试问题。

要求：
1. 技术类问题：从基础到深入的阶梯式设计
2. 行为类问题：使用 STAR 方法论（Situation-Task-Action-Result）
3. 情景类问题：模拟实际工作场景
4. 开放类问题：考察思维方式和价值观

每个问题需包含：
- question: 具体问题
- category: 分类（技术/行为/情景/开放）
- difficulty: 难度（基础/进阶/深入）
- evaluation_points: 评估要点
- ideal_answer_hints: 理想回答的关键点
- follow_up: 追问方向

输出 JSON 数组，至少包含 8 个问题。"""),
        ("user", """岗位 JD：
{jd}

候选人简历摘要：
{resume_summary}

重点考察方向：
{focus_areas}"""),
    ])

    def __init__(self, llm):
        self.llm = llm
        self.json_parser = JsonOutputParser()

    async def generate(
        self,
        jd: str,
        resume_summary: str = "",
        focus_areas: str = "技术能力、团队协作、问题解决",
        num_questions: int = 8,
    ) -> list[InterviewQuestion]:
        """生成面试问题"""
        chain = self.GENERATE_PROMPT | self.llm | self.json_parser
        result = await chain.ainvoke({
            "jd": jd,
            "resume_summary": resume_summary,
            "focus_areas": focus_areas,
        })

        questions = []
        for q in result if isinstance(result, list) else result.get("questions", []):
            questions.append(InterviewQuestion(
                question=q.get("question", ""),
                category=q.get("category", "开放"),
                difficulty=q.get("difficulty", "基础"),
                evaluation_points=q.get("evaluation_points", []),
                ideal_answer_hints=q.get("ideal_answer_hints", ""),
                follow_up=q.get("follow_up", ""),
            ))

        return questions[:num_questions]
```

#### 招聘邮件起草

```python
"""hr/email_drafter.py — 招聘邮件起草"""

from langchain_core.prompts import ChatPromptTemplate


class RecruitmentEmailDrafter:
    """
    招聘邮件起草器

    支持类型：面试邀请、Offer、拒信、背景调查邀请
    """

    TEMPLATES = {
        "interview_invite": ChatPromptTemplate.from_messages([
            ("system", "你是一位专业的 HR，请起草一封面试邀请邮件。语气专业友好，内容简洁明了。"),
            ("user", """候选人姓名：{name}
应聘岗位：{position}
面试时间：{interview_time}
面试地点/方式：{interview_location}
面试官：{interviewers}
备注：{notes}"""),
        ]),

        "offer": ChatPromptTemplate.from_messages([
            ("system", "你是一位专业的 HR，请起草一封 Offer 邮件。语气热情诚恳，突出公司优势。"),
            ("user", """候选人姓名：{name}
岗位：{position}
部门：{department}
薪资范围：{salary}
入职日期：{start_date}
其他福利：{benefits}"""),
        ]),

        "rejection": ChatPromptTemplate.from_messages([
            ("system", "你是一位专业的 HR，请起草一封婉拒邮件。语气礼貌尊重，适当鼓励。"),
            ("user", """候选人姓名：{name}
应聘岗位：{position}
拒绝原因（内部参考，不要直接写入邮件）：{reason}"""),
        ]),
    }

    def __init__(self, llm):
        self.llm = llm

    async def draft(self, email_type: str, **kwargs) -> str:
        """起草指定类型的邮件"""
        if email_type not in self.TEMPLATES:
            raise ValueError(f"不支持的邮件类型: {email_type}，"
                           f"可选: {list(self.TEMPLATES.keys())}")
        prompt = self.TEMPLATES[email_type]
        chain = prompt | self.llm
        result = await chain.ainvoke(kwargs)
        return result.content
```

#### 人才库搜索

```python
"""hr/talent_pool.py — 人才库管理与搜索"""

import json
from pathlib import Path
from datetime import datetime

import chromadb
from langchain_core.prompts import ChatPromptTemplate


class TalentPool:
    """
    人才库 — 使用向量搜索查找历史候选人

    将所有筛选过的简历存入向量库，支持语义搜索。
    例如："找一个有 3 年 Python 经验的后端工程师"
    """

    def __init__(self, persist_dir: str = "./data/talent_pool"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name="talent_pool",
            metadata={"hnsw:space": "cosine"},
        )

    def add_candidate(
        self,
        candidate_id: str,
        resume_text: str,
        metadata: dict = None,
    ):
        """添加候选人到人才库"""
        meta = metadata or {}
        meta["added_at"] = datetime.now().isoformat()

        self.collection.upsert(
            documents=[resume_text],
            metadatas=[meta],
            ids=[candidate_id],
        )

    def search(
        self, query: str, top_k: int = 10, filters: dict = None
    ) -> list[dict]:
        """
        语义搜索人才库

        Args:
            query: 搜索描述，如"3年Python后端经验"
            top_k: 返回结果数量
            filters: ChromaDB where 过滤条件

        Returns:
            匹配的候选人列表
        """
        kwargs = {
            "query_texts": [query],
            "n_results": min(top_k, self.collection.count() or 1),
        }
        if filters:
            kwargs["where"] = filters

        results = self.collection.query(**kwargs)

        candidates = []
        if results["ids"] and results["ids"][0]:
            for i, cid in enumerate(results["ids"][0]):
                candidates.append({
                    "candidate_id": cid,
                    "resume_text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "similarity": 1 - results["distances"][0][i],
                })

        return candidates

    def get_stats(self) -> dict:
        """获取人才库统计信息"""
        return {
            "total_candidates": self.collection.count(),
        }
```

### 5.5 音频转文字与 PDF 转 MD

> [!warning] 依赖说明
> 音频转文字需要安装 `openai-whisper` 或使用在线 API。PDF 转 Markdown 推荐 `pymupdf4llm` 或 `pdfplumber`，效果比纯 `PyPDF2` 好很多。

```python
"""tools/converters.py — 格式转换工具"""

from pathlib import Path
from .base import BaseTool, ToolResult


class PDFToMarkdownTool(BaseTool):
    """PDF 转 Markdown 工具"""
    name = "pdf_to_markdown"
    description = "将 PDF 文件转为 Markdown 格式（常用于简历解析）"

    async def execute(self, pdf_path: str, output_path: str = "") -> ToolResult:
        """
        将 PDF 转为 Markdown

        使用 pymupdf4llm 进行转换，保留格式和结构。
        """
        try:
            import pymupdf4llm

            md_text = pymupdf4llm.to_markdown(pdf_path)

            if output_path:
                Path(output_path).write_text(md_text, encoding="utf-8")
                return ToolResult(
                    success=True,
                    data=f"已转换并保存到 {output_path}，共 {len(md_text)} 字符",
                )
            return ToolResult(success=True, data=md_text)

        except ImportError:
            # 回退方案：使用 pdfplumber
            try:
                import pdfplumber

                text_parts = []
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            text_parts.append(text)

                md_text = "\n\n---\n\n".join(text_parts)
                if output_path:
                    Path(output_path).write_text(md_text, encoding="utf-8")
                return ToolResult(success=True, data=md_text)

            except ImportError:
                return ToolResult(
                    success=False, data=None,
                    error="请安装 pymupdf4llm 或 pdfplumber: pip install pymupdf4llm",
                )
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))


class AudioToTextTool(BaseTool):
    """音频转文字工具"""
    name = "audio_to_text"
    description = "将音频文件转为文字（用于面试录音转录）"

    async def execute(
        self, audio_path: str, model_size: str = "base", language: str = "zh"
    ) -> ToolResult:
        """
        使用 Whisper 模型将音频转为文字

        Args:
            audio_path: 音频文件路径
            model_size: Whisper 模型大小 (tiny/base/small/medium/large)
            language: 语言代码
        """
        try:
            import whisper

            model = whisper.load_model(model_size)
            result = model.transcribe(
                audio_path,
                language=language,
                verbose=False,
            )

            text = result["text"]
            segments = result.get("segments", [])

            # 带时间戳的完整转录
            timestamped = []
            for seg in segments:
                start = self._format_time(seg["start"])
                end = self._format_time(seg["end"])
                timestamped.append(f"[{start} → {end}] {seg['text'].strip()}")

            return ToolResult(
                success=True,
                data={
                    "text": text,
                    "timestamped": "\n".join(timestamped),
                    "duration": segments[-1]["end"] if segments else 0,
                },
            )
        except ImportError:
            return ToolResult(
                success=False, data=None,
                error="请安装 openai-whisper: pip install openai-whisper",
            )
        except Exception as e:
            return ToolResult(success=False, data=None, error=str(e))

    @staticmethod
    def _format_time(seconds: float) -> str:
        """将秒数格式化为 MM:SS"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
```

### 5.6 测试策略与测试用例

> [!tip] 测试分层
> 按照赋范课堂的建议，测试分三层：**单元测试**（各模块独立功能）、**集成测试**（模块间协作）、**端到端测试**（完整对话流程）。LLM 相关的测试用 mock 替代，避免测试依赖外部 API。

```python
"""tests/test_memory.py — 记忆系统测试"""

import pytest
import tempfile
from pathlib import Path

from src.memory.manager import MemoryManager, MemoryConfig
from src.memory.chunker import chunk_text, Chunk
from src.memory.persistent import PersistentMemory
from src.memory.session import SessionMemory


class TestChunker:
    """文本分块器测试"""

    def test_basic_chunking(self):
        """测试基本分块功能"""
        text = "这是第一段。\n\n这是第二段。\n\n这是第三段。"
        chunks = chunk_text(text, chunk_size=10, chunk_overlap=2)
        assert len(chunks) > 0
        assert all(isinstance(c, Chunk) for c in chunks)

    def test_overlap(self):
        """测试分块重叠"""
        text = "A" * 1000 + "\n\n" + "B" * 1000
        chunks = chunk_text(text, chunk_size=200, chunk_overlap=50)
        # 验证相邻块有重叠
        if len(chunks) >= 2:
            assert chunks[0].text[-20:] in chunks[1].text or \
                   len(chunks[0].text) <= 200 * 1.5

    def test_empty_text(self):
        """测试空文本"""
        chunks = chunk_text("")
        assert len(chunks) == 0

    def test_short_text(self):
        """短文本不应被分块"""
        text = "这是一小段文字。"
        chunks = chunk_text(text, chunk_size=400)
        assert len(chunks) == 1


class TestPersistentMemory:
    """持久记忆测试"""

    def test_initialize(self, tmp_path):
        """测试初始化创建 MEMORY.md"""
        filepath = tmp_path / "MEMORY.md"
        mem = PersistentMemory(filepath)
        assert filepath.exists()
        content = mem.read()
        assert "# Auto Memory" in content

    def test_append_section(self, tmp_path):
        """测试追加记忆段落"""
        filepath = tmp_path / "MEMORY.md"
        mem = PersistentMemory(filepath)
        mem.append_section("测试标题", "测试内容")
        content = mem.read()
        assert "测试标题" in content
        assert "测试内容" in content

    def test_update_preference(self, tmp_path):
        """测试更新用户偏好"""
        filepath = tmp_path / "MEMORY.md"
        mem = PersistentMemory(filepath)
        mem.update_preference("语言", "中文")
        content = mem.read()
        assert "**语言**: 中文" in content


class TestSessionMemory:
    """会话记忆测试"""

    def test_append_and_retrieve(self, tmp_path):
        """测试写入和读取"""
        mem = SessionMemory(tmp_path / "sessions")
        mem.append("test-001", {"role": "user", "content": "你好"})
        mem.append("test-001", {"role": "assistant", "content": "你好！"})
        messages = mem.get_all("test-001")
        assert len(messages) == 2
        assert messages[0]["content"] == "你好"

    def test_get_recent(self, tmp_path):
        """测试获取最近 N 条"""
        mem = SessionMemory(tmp_path / "sessions")
        for i in range(20):
            mem.append("test-002", {"role": "user", "content": f"消息{i}"})
        recent = mem.get_recent("test-002", n=5)
        assert len(recent) == 5
        assert recent[0]["content"] == "消息15"

    def test_truncate(self, tmp_path):
        """测试截断功能"""
        mem = SessionMemory(tmp_path / "sessions")
        for i in range(20):
            mem.append("test-003", {"role": "user", "content": f"消息{i}"})
        mem.truncate("test-003", keep_recent=3)
        remaining = mem.get_all("test-003")
        assert len(remaining) == 3

    def test_nonexistent_session(self, tmp_path):
        """测试查询不存在的会话"""
        mem = SessionMemory(tmp_path / "sessions")
        messages = mem.get_all("nonexistent")
        assert messages == []


class TestMemoryManager:
    """记忆管理器集成测试"""

    @pytest.fixture
    def manager(self, tmp_path):
        config = MemoryConfig(base_dir=str(tmp_path / "memory"))
        return MemoryManager(config=config)

    @pytest.mark.asyncio
    async def test_add_message(self, manager):
        """测试添加消息到记忆系统"""
        await manager.add_message(
            role="user",
            content="你好，我想找一位 Python 工程师",
            session_id="session-001",
        )
        context = manager.get_session_context("session-001")
        assert len(context) == 1

    @pytest.mark.asyncio
    async def test_flush_threshold(self, manager):
        """测试 80% 阈值触发刷写"""
        manager.config.max_context_tokens = 100
        manager.config.context_flush_threshold = 0.3  # 30% 方便测试

        for i in range(10):
            await manager.add_message(
                role="user",
                content=f"这是一条比较长的测试消息，编号 {i}，" * 5,
                session_id="session-flush",
            )

        # 检查持久记忆是否有写入
        content = manager.persistent.read()
        # 如果触发了刷写，MEMORY.md 中应有会话摘要
        # （取决于 token 计数是否超过阈值）
```

```python
"""tests/test_hr.py — HR 功能测试"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.hr.resume_parser import ResumeScreener, ScreeningResult
from src.hr.evaluator import CandidateEvaluator, EvaluationReport
from src.hr.interviewer import InterviewQuestionGenerator
from src.hr.talent_pool import TalentPool


SAMPLE_RESUME = """
张三
手机：138-0000-0000 | 邮箱：zhangsan@example.com

教育背景
- 北京大学 计算机科学与技术 硕士 2020年毕业

工作经历
1. 字节跳动 — 高级后端工程师 (2020-2024)
   - 负责推荐系统核心服务开发，日均处理 10 亿次请求
   - 使用 Python/Go 开发微服务，熟悉 Kubernetes 部署
   - 带领 5 人小组完成系统架构升级，性能提升 40%

2. 百度 — 后端工程师实习 (2019)
   - 参与搜索引擎索引服务开发

技术栈
Python, Go, Kubernetes, Docker, Redis, MySQL, Kafka, gRPC
"""

SAMPLE_JD = """
岗位：高级 Python 后端工程师
要求：
- 本科及以上学历，计算机相关专业
- 3 年以上 Python 后端开发经验
- 熟悉分布式系统设计
- 熟悉 Docker/Kubernetes
- 有大规模系统开发经验优先
"""


class TestResumeScreener:
    """简历筛选测试"""

    @pytest.fixture
    def mock_llm(self):
        llm = AsyncMock()
        return llm

    @pytest.mark.asyncio
    async def test_screen_resume_returns_result(self, mock_llm):
        """测试筛选返回正确格式"""
        # Mock LLM 返回
        mock_llm.ainvoke = AsyncMock(return_value=MagicMock(
            content='{"overall_score": 85, "skill_match": 90, '
                    '"experience_match": 80, "education_match": 85, '
                    '"recommendation": "强烈推荐", '
                    '"highlights": ["大厂经验", "技术栈匹配"], '
                    '"concerns": [], "reasoning": "高度匹配"}'
        ))

        # 注意：实际测试需要更完整的 mock chain
        # 此处展示测试结构和预期行为


class TestTalentPool:
    """人才库测试"""

    @pytest.fixture
    def pool(self, tmp_path):
        return TalentPool(persist_dir=str(tmp_path / "talent"))

    def test_add_and_search(self, pool):
        """测试添加候选人并搜索"""
        pool.add_candidate(
            candidate_id="c001",
            resume_text=SAMPLE_RESUME,
            metadata={"position": "后端工程师"},
        )

        results = pool.search("Python 后端 分布式", top_k=5)
        assert len(results) >= 1
        assert results[0]["candidate_id"] == "c001"
        assert results[0]["similarity"] > 0

    def test_stats(self, pool):
        """测试统计信息"""
        pool.add_candidate("c001", "简历1")
        pool.add_candidate("c002", "简历2")
        stats = pool.get_stats()
        assert stats["total_candidates"] == 2
```

---

## Part 6: 关键配置文件模板

> 对应赋范课堂贯穿全系列的配置实践

### 6.1 openclaw.json 完整模板（带注释）

> [!note] 说明
> 这是原版 OpenClaw 的配置文件模板，用于理解原版架构。Mini 版使用 `settings.yaml` + `.env`。

```json
{
  // --- 基础配置 ---
  "name": "my-openclaw-instance",
  "version": "1.0.0",

  // --- Gateway 配置 ---
  "gateway": {
    "host": "127.0.0.1",
    "port": 18789,                    // 默认 WebSocket 端口
    "protocol": "ws",
    "maxConcurrentSessions": 50,
    "sessionTimeout": 3600000,        // 会话超时 1 小时（毫秒）
    "healthCheckInterval": 30000      // 健康检查间隔 30 秒
  },

  // --- LLM Provider 配置 ---
  "providers": {
    "default": "anthropic/claude-sonnet-4",
    "fallback": "openai/gpt-4o",
    "models": {
      "anthropic/claude-sonnet-4": {
        "temperature": 0.7,
        "maxTokens": 4096,
        "streaming": true
      },
      "deepseek/deepseek-chat": {
        "temperature": 0.3,
        "maxTokens": 8192,
        "streaming": true,
        "baseUrl": "https://api.deepseek.com/v1"
      }
    }
  },

  // --- 记忆系统配置 ---
  "memory": {
    "persistent": {
      "file": "MEMORY.md",
      "maxSize": "1MB"
    },
    "temporal": {
      "directory": "memory/",
      "retentionDays": 90
    },
    "session": {
      "directory": "sessions/",
      "format": "jsonl"
    },
    "embedding": {
      "priority": ["local-gguf", "openai", "gemini", "voyage", "mistral"],
      "localModel": "nomic-embed-text-v1.5.Q8_0.gguf",
      "chunkSize": 400,
      "chunkOverlap": 80
    },
    "search": {
      "vectorWeight": 0.7,
      "bm25Weight": 0.3,
      "mmrLambda": 0.7,
      "temporalDecayHalfLife": 30,
      "contextFlushThreshold": 0.8
    }
  },

  // --- 工具系统配置 ---
  "tools": {
    "groups": ["runtime", "fs", "web", "ui", "messaging", "sessions", "memory", "automation"],
    "cascadePolicy": {
      "levels": ["global-deny", "provider", "agent", "sandbox", "owner-only"],
      "defaultLevel": "sandbox"
    },
    "sandbox": {
      "enabled": true,
      "timeout": 30000,
      "maxMemory": "256MB"
    }
  },

  // --- Skills 配置 ---
  "skills": {
    "directory": "skills/",
    "autoLoad": true,
    "maxActiveSkills": 5
  },

  // --- Channel 配置 ---
  "channels": {
    "enabled": ["web", "telegram"],
    "web": {
      "port": 3000,
      "corsOrigins": ["http://localhost:*"]
    }
  }
}
```

### 6.2 AGENTS.md 模板（HR Agent 版）

```markdown
---
name: hr_agent
display_name: 小招 — AI 招聘助手
model: deepseek/deepseek-chat
temperature: 0.3
max_tokens: 4096
tools:
  - file_read
  - file_write
  - web_search
  - pdf_to_markdown
  - audio_to_text
skills:
  - hr_recruitment
memory:
  persistent: true
  temporal: true
  session_window: 50
---

# 小招 — AI 招聘助手

## 核心职责
你是"小招"，服务于 HR 团队的 AI 招聘助手。你的核心职责是：
1. 高效筛选和评估候选人简历
2. 生成有针对性的面试问题
3. 起草专业的招聘相关邮件
4. 管理和搜索人才库
5. 将面试录音转为文字记录

## 工作原则
- 客观公正，基于能力和经验评估
- 保护候选人隐私，遵守劳动法规
- 输出结构化、可操作的结果
- 主动识别风险并给出建议

## 输出规范
- 使用 Markdown 格式
- 关键数据用表格呈现
- 评分用量化指标
- 重要结论加粗标注
```

### 6.3 SOUL.md 模板（HR Agent 版）

```markdown
---
agent: hr_agent
type: soul
version: 1.0
---

# 小招的灵魂设定

## 身份认知
我是"小招"，一位 AI 驱动的招聘助手。我服务于 HR 团队，帮助他们更高效、更精准地完成招聘工作。

## 性格特质
- **专业**：对招聘流程和人才评估有深入理解
- **细致**：不放过简历中的任何关键信息
- **公正**：评估时不受无关因素干扰
- **温和**：使用专业但亲切的语言沟通

## 能力边界
- 我能做：简历解析、候选人评估、问题生成、邮件起草、人才搜索
- 我不能做：最终录用决策、薪资谈判、背景调查执行
- 我会提醒：涉及法律合规风险时主动告警

## 沟通风格
- 简洁高效，避免冗余
- 结构化输出，善用表格和列表
- 关键判断一定给出理由
- 不确定的信息会明确标注
```

### 6.4 USER.md 模板

```markdown
---
type: user
---

# 用户配置

## 基本信息
- 角色：HR 经理
- 公司：[公司名]
- 行业：[行业]

## 招聘偏好
- 重点关注：技术能力 > 文化匹配 > 学历背景
- 面试风格：结构化面试 + STAR 行为面试法
- 沟通语言：中文

## 常用岗位
- 后端工程师
- 前端工程师
- 数据分析师
- 产品经理

## 特殊要求
- 简历筛选结果需要导出为表格
- 面试问题按难度分级
- 邮件风格专业但友好
```

### 6.5 SKILL.md 模板（HR Recruitment Skill）

```markdown
---
name: hr_recruitment
display_name: HR 招聘全流程
description: 完整的 HR 招聘辅助技能，覆盖简历筛选、评估、面试、邮件全流程
version: 1.0.0
author: mini-openclaw
tags: [hr, recruitment, 招聘, 面试, 简历]
gate:
  - type: keyword
    keywords: [简历, 招聘, 候选人, 面试, HR, 人才, offer, JD, 岗位]
  - type: intent
    intents: [screen_resume, evaluate_candidate, generate_questions, draft_email, search_talent]
tools:
  - file_read
  - file_write
  - web_search
  - pdf_to_markdown
  - audio_to_text
priority: 10
---

# HR 招聘全流程技能

## 功能清单

### 1. 简历筛选
当用户提供简历和 JD 时，执行以下流程：
- 解析简历为结构化数据
- 与 JD 进行多维度匹配
- 输出匹配度评分和推荐等级
- 标注亮点和顾虑

### 2. 候选人评估
从以下四个维度进行综合评估：
- 技术能力（0-10分）
- 文化匹配度（0-10分）
- 成长潜力（0-10分）
- 沟通能力（0-10分）

### 3. 面试问题生成
根据岗位和候选人背景生成问题：
- 技术类：基础 → 进阶 → 深入
- 行为类：STAR 方法论
- 情景类：模拟工作场景
- 开放类：考察思维方式

### 4. 邮件起草
支持以下邮件类型：
- 面试邀请（interview_invite）
- Offer 发放（offer）
- 婉拒通知（rejection）

### 5. 人才库
- 添加候选人到人才库
- 语义搜索历史候选人
- 支持条件过滤

## 输出格式规范
- 所有评估结果使用 Markdown 表格
- 评分使用数值 + 文字说明
- 面试问题按难度分组
- 邮件输出完整格式（含主题行）
```

---

## 相关笔记

- [[docs/OpenClaw 完整技术架构与应用详解.md|OpenClaw 完整技术架构与应用详解]] — 原版 OpenClaw 的完整架构拆解
- [[Research/OpenClaw-技术原理拆解-小白版.md|OpenClaw 技术原理拆解（小白版）]] — 面向初学者的技术原理解读
- [[docs/OpenClaw-视频攻略-赋范课堂28集.md|OpenClaw 视频攻略（赋范课堂28集）]] — 28 集视频教程的完整笔记

---

> [!quote] 开发感悟
> "不要试图一次性复刻整个 OpenClaw。找到你业务需要的那 20% 核心功能，用 Python 生态快速实现它，然后在实际使用中迭代。" — 赋范课堂 P8
