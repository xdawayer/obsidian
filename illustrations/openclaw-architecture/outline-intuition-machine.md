# 插图方案：Intuition Machine 风格（技术简报）

**文章**: docs/OpenClaw 完整技术架构与应用详解.md
**风格**: intuition-machine — 学术技术简报风格，泛黄纸张质感，中英双语标注
**配色**: 旧纸色(#F5F0E6) + 青蓝(#2F7373) + 棕褐(#8B7355) + 深红(#722F37)
**插图数量**: 10 张

---

## 插图 1：OpenClaw 全景概念图

**插入位置**: 第一部分「OpenClaw 是什么」标题之后
**目的**: 学术风格的技术概览，建立专业感
**视觉内容**: 等距视图的系统架构鸟瞰图。中心标注"OpenClaw — 开源自治AI Agent平台 / Open-Source Autonomous AI Agent Platform"。六个模块以放射状排列，每个都有中英双语标签：消息通道/Channels、网关/Gateway、模型/LLM Providers、工具/Tools、记忆/Memory、编排/Orchestration。底部引用"GitHub 175K+ ★ · MIT License · TypeScript"
**文件名**: illustration-openclaw-overview.png

---

## 插图 2：三层架构剖面

**插入位置**: 第二部分「核心架构」ASCII 图之前
**目的**: 专业级的架构剖面图
**视觉内容**: 三层水平切面图，复古工程图风格。Layer 1/通道层(Channel Layer)：50+平台图标排列。Layer 2/网关层(Gateway Layer)：核心控制平面，内部标注6个子模块。Layer 3/模型层(LLM Provider Layer)：多个AI引擎。层间用标注线连接，标注数据格式(StandardMessage/结构化上下文)。右侧文字框说明"Hub-and-Spoke 轴辐式架构"
**文件名**: illustration-three-layer-arch.png

---

## 插图 3：消息处理六阶段

**插入位置**: 第二部分「消息处理六阶段流水线」段落之后
**目的**: 精密的流水线技术图解
**视觉内容**: 水平管道流程图，6个处理节点。每个节点是一个标注框，包含中英双语名称和关键操作。①Ingestion/摄入 → ②Access Control/访问控制 → ③Session Resolution/会话解析 → ④Context Assembly/上下文组装 → ⑤Model Invocation/模型调用 → ⑥Response Delivery/响应投递。管道用青蓝色渐进
**文件名**: illustration-six-stage-pipeline.png

---

## 插图 4：Agent 运行时四阶段

**插入位置**: 第三部分「Agent 运行四阶段」ASCII 图之前
**目的**: 展示Agent的完整执行生命周期
**视觉内容**: 四个分区面板横向排列。Phase 1/上下文组装：文件堆叠图示。Phase 2/模型推理：神经网络简笔。Phase 3/工具执行：齿轮+沙箱示意。Phase 4/状态持久化：数据库+文件写入。每个面板包含关键子步骤的双语标签。底部标注"Agent Loop — 思考→行动→观察→持久化"
**文件名**: illustration-agent-four-phases.png

---

## 插图 5：工具系统拓扑

**插入位置**: 第三部分「工具系统（Function Calling）」表格之后
**目的**: 展示工具组织架构和Function Calling机制
**视觉内容**: 中心Agent核心，8个工具组以辐射拓扑连接。每个工具组用技术图标+中英双语标签。底部展示Function Calling五级权限级联(Global → Provider → Agent → Sandbox → Owner-only)，用层次递进表示。标注框说明"拒绝列表永远优先 / Deny list always wins"
**文件名**: illustration-tool-system.png

---

## 插图 6：三层记忆架构

**插入位置**: 第四部分「三层记忆架构」ASCII 图之前
**目的**: 核心创新的学术级图解
**视觉内容**: 三层堆叠的数据库切面。Layer 1 持久记忆/Persistent Memory：MEMORY.md，标注"策划的长期知识"。Layer 2 临时记忆/Ephemeral Memory：memory/YYYY-MM-DD.md。Layer 3 会话记忆/Session Memory：sessions/*.jsonl。右侧展示混合搜索引擎：Vector Search(0.7) + BM25(0.3) → MMR重排序 → 时间衰减。底部标注"SQLite + sqlite-vec"
**文件名**: illustration-memory-three-layers.png

---

## 插图 7：压缩前记忆刷写

**插入位置**: 第四部分「上下文窗口管理：压缩前记忆刷写」段落之后
**目的**: 图解OpenClaw最关键的记忆创新
**视觉内容**: 时间线流程图。左：Context Window(176K/200K token)进度条达到80%红线。中：触发"Silent Agent Turn/静默代理回合"，AI提取关键信息写入memory/文件。右：旧消息被安全压缩，但关键信息已存在外部。标注框："记忆存储在上下文窗口外部 / Memory persists outside context window"。底部对比：传统AI(压缩=失忆) vs OpenClaw(压缩前刷写=永不失忆)
**文件名**: illustration-memory-flush.png

---

## 插图 8：多Agent编排拓扑

**插入位置**: 第五部分「多 Agent 编排」整节开头
**目的**: 展示Agent集群的协作网络
**视觉内容**: 网络拓扑图。主Agent(Zoe)在中心，三条spawn线连接到子Agent(Codex/Claude Code/Gemini)。Agent间有sessions_send双向通信线。右侧面板展示Lobster工作流引擎：YAML确定性步骤 → 条件循环 → 通知。关键标注："确定性编排 + 创造性执行 / Deterministic Orchestration + Creative Execution"
**文件名**: illustration-multi-agent-topology.png

---

## 插图 9：Elvis双层架构

**插入位置**: 第七部分「双层设计」ASCII 图之前
**目的**: 案例核心架构的学术级展示
**视觉内容**: 上下双层框架图。上层/Orchestration Layer(编排层)：Zoe Agent居中，4条连接线到Obsidian/会议记录/生产DB(只读)/管理API。标签"持有全部业务上下文 / Holds full business context"。下层/Execution Layer(执行层)：3个独立工作区(Codex 90%/Claude Code/Gemini)。标签"最小上下文原则 / Minimal context principle"。层间标注"精确Prompt传递 / Precise prompt delivery"
**文件名**: illustration-elvis-two-layer.png

---

## 插图 10：竞品对比矩阵

**插入位置**: 第十部分「与竞品对比」表格之后
**目的**: 多维度可视化对比
**视觉内容**: 雷达/蛛网图，5个维度(中英双语)：定制化Customization、记忆Memory、主动性Proactivity、安全Security、成本Cost-efficiency。四条数据线：OpenClaw(青蓝实线)、Devin(棕褐虚线)、Claude Code(深红虚线)、n8n(灰色虚线)。右侧图例框。标注OpenClaw在记忆和主动性上的显著优势
**文件名**: illustration-competitor-radar.png
