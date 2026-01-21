# schema-markup

来源: /Users/wzb/obsidian/marketingskills/skills/schema-markup/SKILL.md

## 技能触发（prompt 意图）
- 用户要做 schema/结构化数据/JSON-LD/富结果/FAQ schema/product schema/breadcrumb schema。

## 一句话范围
实现准确合规的 JSON-LD 结构化数据，以提升搜索理解与富结果展示。

## Prompt 结构深度解读
1. 初始评估
   - 页面类型、当前 schema、目标富结果。
2. 核心原则
   - 准确性优先、JSON-LD、遵循 Google 规范、全量校验。
3. 常见 schema 类型
   - Organization、WebSite、Article、Product、SoftwareApplication、FAQ、HowTo、BreadcrumbList、LocalBusiness、Review、Event。
4. 多类型 schema
   - 使用 @graph 组合多个实体。
5. 验证与测试
   - Rich Results Test 与 schema.org validator。
6. 实施模式
   - 静态站点、React/Next.js SSR、CMS 插件。
7. 输出格式
   - JSON-LD 代码块 + 放置位置 + 测试清单。
8. 问题与相关技能
   - seo-audit、programmatic-seo、analytics-tracking。

## 适用场景
- “给价格页加 FAQ schema。”
- “SaaS 需要 Product/SoftwareApplication schema。”
- “修复 Search Console 的 schema 报错。”

## 使用方式（分步）
1. 确认页面类型与意图
   - 选择与可见内容一致的 schema 类型。
2. 审核已有标记
   - 识别现有 schema 与错误。
3. 选定 schema 类型
   - 对照必填字段与推荐字段。
4. 编写 JSON-LD
   - 数据真实、字段完整。
5. 正确放置
   - 放在 head 或 body 末尾，前端框架需 SSR。
6. 上线前验证
   - Rich Results Test、Schema Validator。
7. Search Console 监控
   - 及时修复错误与警告。

## 输出期望
- 适配页面的完整 JSON-LD。
- 放置与验证步骤说明。

## 常见误区
- 标注页面不存在的内容。
- 缺少必填字段或使用不支持类型。
- 内容变更后不更新 schema。

## 适合搭配的技能
- seo-audit: 结构化数据审计与修复。
- programmatic-seo: 模板化批量 schema。
