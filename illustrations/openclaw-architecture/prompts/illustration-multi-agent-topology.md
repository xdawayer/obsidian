插图主题：多 Agent 编排拓扑
风格：blueprint — 精密工程蓝图风格

视觉构图：
- 主视觉：树形/网络拓扑图，展示多 Agent 协作
- 布局：
  - 顶部中心：主 Agent 节点 (Zoe)，用深蓝(#1E3A5F)大圆表示
    标注："Main Agent (Zoe) — 编排者"
  - 下方三条 spawn 分支线连接到三个子 Agent：
    · 左：Codex Agent — 标注 "后端开发"
    · 中：Claude Code Agent — 标注 "前端开发"
    · 右：Gemini Agent — 标注 "UI 设计"
  - 子 Agent 之间有水平双向箭头，标注 "sessions_send 双向通信"
  - spawn 线上标注 "spawn_agent()" 函数调用
- 右侧独立面板：Lobster 工作流引擎
  - YAML 图标 → "确定性步骤定义"
  - 流程图标 → "条件循环"
  - 通知图标 → "状态通知"
  - 底部标注："确定性编排 + 创造性执行 / Deterministic Orchestration + Creative Execution"

配色方案：
- 主色：工程蓝 #2563EB
- 背景：蓝图纸白底 #FAF8F5
- 主 Agent：深蓝 #1E3A5F
- 子 Agent：工程蓝 #2563EB
- spawn 线：实线蓝色
- 通信线：虚线蓝色
- Lobster 面板：浅蓝 #BFDBFE 背景
- 文字：深灰 #334155

文字内容：
- Agent 名称和角色标注
- spawn_agent() 函数标注
- sessions_send 通信标注
- Lobster 工作流说明

风格要点：树形拓扑，主从关系清晰。spawn 线用实线，通信线用虚线区分。右侧 Lobster 面板独立但视觉统一。
