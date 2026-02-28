插图主题：Elvis 双层架构
风格：blueprint — 精密工程蓝图风格

视觉构图：
- 主视觉：上下双层蓝图框架，展示编排层和执行层分离
- 布局：
  - 上层 — 编排层 / Orchestration Layer：
    深蓝(#1E3A5F)边框大框
    中心：Zoe Agent 节点（圆形）
    四条连接线连接到四个数据源：
    · 左上：Obsidian 知识库图标
    · 右上：会议记录图标
    · 左下：生产数据库图标（标注"只读"）
    · 右下：管理员 API 图标
    框内右侧标注："持有全部业务上下文 / Holds full business context"
  - 下层 — 执行层 / Execution Layer：
    工程蓝(#2563EB)边框大框
    内部三个独立工作区（矩形子框）：
    · Codex Agent (90%) — 标注 "独立 worktree"
    · Claude Code Agent — 标注 "独立 worktree"
    · Gemini Agent — 标注 "独立 worktree"
    框内右侧标注："最小上下文原则 / Minimal context principle"
  - 两层之间：精确的向下箭头，标注 "精确 Prompt 传递 / Precise prompt delivery"
  - 隔离线标注：编排层与执行层之间有明确的分隔线

配色方案：
- 主色：工程蓝 #2563EB
- 背景：蓝图纸白底 #FAF8F5
- 编排层边框：深蓝 #1E3A5F
- 执行层边框：工程蓝 #2563EB
- 工作区填充：浅蓝 #BFDBFE
- Zoe 节点：深蓝实心
- 文字：深灰 #334155

文字内容：
- 双层中英双语标注
- 数据源标签
- 工作区名称和占比
- 核心原则标注

风格要点：上下双层，编排层用更深的颜色表示更高层级。层间箭头强调"精确传递"的设计理念。执行层三个工作区完全隔离，用独立边框表示。
