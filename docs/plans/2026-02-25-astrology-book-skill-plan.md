# Astrology Book Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create `astrology-book-skill` — a specialized skill for deconstructing astrology books into bilingual (Chinese + English) deep-analysis notes.

**Architecture:** Single skill with separated reference files. SKILL.md defines the workflow and shared rules. Chinese and English templates live in separate reference files (`type-templates-cn.md` / `type-templates-en.md`). A custom `validate.sh` checks both output files. Reuses proven patterns from the existing `book-deconstruction-skill`.

**Tech Stack:** Markdown skill files, Bash validation script (with perl for CJK char counting and English word counting)

**Status:** All 8 implementation tasks completed. Skill smoke-tested and operational.

---

## Execution Log

### Skill Implementation (Tasks 1-8): COMPLETED

All 8 tasks executed via subagent-driven development on 2026-02-25.

### Book Deconstruction Batch 1: 5 Books COMPLETED

| # | Book | Subtype | CN Status | EN Status | Validation |
|---|------|---------|-----------|-----------|------------|
| 1 | The Inner Sky — Steven Forrest | 入门教程 | 6506字 | 3083 words | 47/47 |
| 2 | Saturn: A New Look at an Old Devil — Liz Greene | 心理占星 | 8255字 | 4221 words | 47/47 |
| 3 | Yesterday's Sky — Steven Forrest | 演化占星 | 8191字 | 4348 words | 47/47 |
| 4 | Cosmos and Psyche — Richard Tarnas | 占星哲学与历史 | 10156字 | 5023 words | 47/47 |
| 5 | Mythic Astrology — Ariel Guttman & Kenneth Johnson | 神话与原型 | 8961字 | 4352 words | 47/47 |

All 10 files passed validation (47/47). Fix applied: English overview blockquote format (3 files).

### Book Deconstruction Batch 2: 5 Books COMPLETED

| # | Book | Subtype | CN Status | EN Status | Validation |
|---|------|---------|-----------|-----------|------------|
| 6 | Planets in Transit — Robert Hand | 行运与预测 | 8852字 | 4106 words | 47/47 |
| 7 | The Twelve Houses — Howard Sasportas | 心理占星 | 10848字 | 5117 words | 47/47 |
| 8 | Astrology, Psychology, and the Four Elements — Stephen Arroyo | 入门教程 | 8960字 | 3548 words | 47/47 |
| 9 | Pluto: The Evolutionary Journey of the Soul — Jeffrey Wolf Green | 演化占星 | 9391字 | 4725 words | 47/47 |
| 10 | The Astrology of Fate — Liz Greene | 心理占星 | 9045字 | 4914 words | 47/47 |

All 10 files passed validation (47/47). Fix applied: EN "developmental model" → "developmental arc/framework" to avoid false positive on "mental model" substring match.

### Output Files

Batch 1 — Chinese:
- `~/obsidian/占星书/中文/《The Inner Sky》 - Steven Forrest.md`
- `~/obsidian/占星书/中文/《Saturn A New Look at an Old Devil》 - Liz Greene.md`
- `~/obsidian/占星书/中文/《Yesterday's Sky》 - Steven Forrest.md`
- `~/obsidian/占星书/中文/《Cosmos and Psyche》 - Richard Tarnas.md`
- `~/obsidian/占星书/中文/《Mythic Astrology》 - Ariel Guttman & Kenneth Johnson.md`

Batch 1 — English:
- `~/obsidian/占星书/英文/《The Inner Sky》 - Steven Forrest.md`
- `~/obsidian/占星书/英文/《Saturn A New Look at an Old Devil》 - Liz Greene.md`
- `~/obsidian/占星书/英文/《Yesterday's Sky》 - Steven Forrest.md`
- `~/obsidian/占星书/英文/《Cosmos and Psyche》 - Richard Tarnas.md`
- `~/obsidian/占星书/英文/《Mythic Astrology》 - Ariel Guttman & Kenneth Johnson.md`

Batch 2 — Chinese:
- `~/obsidian/占星书/中文/《Planets in Transit》 - Robert Hand.md`
- `~/obsidian/占星书/中文/《The Twelve Houses》 - Howard Sasportas.md`
- `~/obsidian/占星书/中文/《Astrology, Psychology, and the Four Elements》 - Stephen Arroyo.md`
- `~/obsidian/占星书/中文/《Pluto The Evolutionary Journey of the Soul》 - Jeffrey Wolf Green.md`
- `~/obsidian/占星书/中文/《The Astrology of Fate》 - Liz Greene.md`

Batch 2 — English:
- `~/obsidian/占星书/英文/《Planets in Transit》 - Robert Hand.md`
- `~/obsidian/占星书/英文/《The Twelve Houses》 - Howard Sasportas.md`
- `~/obsidian/占星书/英文/《Astrology, Psychology, and the Four Elements》 - Stephen Arroyo.md`
- `~/obsidian/占星书/英文/《Pluto The Evolutionary Journey of the Soul》 - Jeffrey Wolf Green.md`
- `~/obsidian/占星书/英文/《The Astrology of Fate》 - Liz Greene.md`

### Subtype Coverage Summary

| 子类型 | Books Covered |
|--------|--------------|
| 入门教程 | The Inner Sky, Astrology Psychology and the Four Elements |
| 心理占星 | Saturn, The Twelve Houses, The Astrology of Fate |
| 演化占星 | Yesterday's Sky, Pluto: The Evolutionary Journey of the Soul |
| 占星哲学与历史 | Cosmos and Psyche |
| 神话与原型 | Mythic Astrology |
| 行运与预测 | Planets in Transit |

All 6 subtypes now covered. Total: 10 books, 20 files.

---

### Task 1: Create directory structure

**Files:**
- Create: `~/.claude/skills/astrology-book-skill/` (directory)
- Create: `~/.claude/skills/astrology-book-skill/references/` (directory)
- Create: `~/.claude/skills/astrology-book-skill/scripts/` (directory)

**Step 1: Create all directories**

Run:
```bash
mkdir -p ~/.claude/skills/astrology-book-skill/references
mkdir -p ~/.claude/skills/astrology-book-skill/scripts
```

**Step 2: Verify**

Run: `ls -R ~/.claude/skills/astrology-book-skill/`
Expected: `references/` and `scripts/` subdirectories exist

---

### Task 2: Write `references/methodologies.md`

**Files:**
- Create: `~/.claude/skills/astrology-book-skill/references/methodologies.md`
- Reference: `~/.claude/skills/book-deconstruction-skill/references/methodologies.md`

**Step 1: Write the methodologies file**

Copy the 10 analysis methods from the existing skill's `methodologies.md` as-is (they are universal). Then add an astrology-specific methodology matching table at the end:

```markdown
# 内部分析方法论工具箱

> ⚠️ 本文件为 AI 内部参考。所有方法论名称和分析框架**绝不出现在用户可见的输出中**。
> 仅用于指导分析思路，输出时将分析结果融入自然段落。

## 10种分析方法

[Copy all 10 methods exactly from existing file — ① through ⑩]

---

## 占星子类型 × 方法论匹配

| 占星子类型 | 主力方法（重心） | 辅助方法（补充） |
|-----------|---------------|---------------|
| 心理占星 | ②第一性原理 + ③苏格拉底 + ⑩概念网络 | ①费曼 + ⑧反脆弱 |
| 演化占星 | ⑤黄金圈 + ⑩概念网络 + ③苏格拉底 | ①费曼 + ⑧反脆弱 |
| 入门教程 | ④布鲁姆 + ⑨类比迁移 + ①费曼 | ⑥DIKW + ⑧反脆弱 |
| 行运与预测 | ④布鲁姆 + ②第一性原理 + ⑨类比迁移 | ⑥DIKW + ①费曼 |
| 占星哲学与历史 | ②第一性原理 + ③苏格拉底 + ⑩概念网络 | ⑥DIKW + ⑧反脆弱 |
| 神话与原型 | ⑤黄金圈 + ⑩概念网络 + ①费曼 | ③苏格拉底 + ⑨类比迁移 |

### 使用要点

分析时在内部按照匹配的方法论组合思考，但输出时：
- 将多种方法论的分析结果**融合**为连贯段落
- 一个段落可能同时包含第一性原理的追问和反脆弱的边界检验，但读起来是自然的讨论
- 不同方法论不分开呈现，而是服务于同一个叙事流

### 占星领域特别注意

- 讨论占星概念时，区分"象征语言"和"字面理解"——占星是一套象征系统
- 对不同占星学派（现代心理 vs 传统 vs 演化）的分歧，以学术态度呈现多方观点
- 避免将占星术语简化为"迷信/科学"二元对立
```

**Step 2: Verify file exists and content is complete**

Run: `wc -l ~/.claude/skills/astrology-book-skill/references/methodologies.md`
Expected: approximately 70-80 lines

---

### Task 3: Write `references/type-templates-cn.md`

**Files:**
- Create: `~/.claude/skills/astrology-book-skill/references/type-templates-cn.md`

**Step 1: Write the Chinese templates file**

This file contains 6 astrology-specific templates. Each template defines:
- 文体 (writing style)
- 语气 (tone)
- 篇幅参考 (word count range)
- 输出结构 (section structure with descriptions and word counts per section)

The 6 templates are:

#### 1. 心理占星
- **文体**：心灵探索体
- **语气**：深入内在，像一位荣格派分析师在跟你讨论星盘中隐藏的心理动力
- **篇幅参考**：8000-12000字
- **必需章节**（7节）：
  1. `这本书照亮了心灵的哪个角落`（500字。核心心理洞察，这本书揭示了什么无意识动力/心理模式？）
  2. `核心概念图谱`（600字。提炼3-5个核心占星心理学概念，讲清含义和关系。占星术语首次出现附英文。）
  3. `心理动力深度解读`（主体，50-60%。按心理主题组织，每个主题：行星/星座/宫位的象征含义→对应的心理动力→在日常生活中的表现→整合与成长的路径。）
  4. `与荣格心理学的对话`（600字。这本书如何运用/发展荣格的原型、阴影、个体化等概念？）
  5. `实践：在星盘中看见自己`（500字。如何将书中概念应用到自己的星盘解读中。具体到"当你看到XX配置时..."）
  6. `这本书的边界`（400字。诚实讨论局限。）
  7. `延伸阅读`（200字。）

#### 2. 演化占星
- **文体**：灵魂叙事体
- **语气**：深邃但不神秘，像一位经验丰富的演化占星师在讲述灵魂的旅程
- **篇幅参考**：8000-12000字
- **必需章节**（7节）：
  1. `灵魂的追问`（500字。这本书要回答什么关于灵魂演化的核心问题？）
  2. `演化模型全景`（600字。全书的演化框架：灵魂如何通过星盘讲述它的故事？核心概念地图。）
  3. `核心理论深度解读`（主体，50-60%。按演化主题组织：冥王星/南北交点/相位的演化含义→灵魂的意图→业力模式→突破路径。）
  4. `与其他占星学派的对话`（500字。演化占星如何区别于心理占星和传统占星？各自的假设前提是什么？）
  5. `解盘实践`（500字。如何运用书中框架解读星盘中的演化主题。）
  6. `这套理论的边界`（400字。诚实讨论"灵魂""前世"等概念的可验证性问题。）
  7. `延伸阅读`（200字。）

#### 3. 入门教程
- **文体**：导学体
- **语气**：清晰友好，像一位有耐心的占星老师带你从零开始
- **篇幅参考**：5000-8000字
- **必需章节**（7节）：
  1. `这本书带你入门什么`（400字。这本书的定位和适合的读者。）
  2. `知识框架`（500字。全书知识体系的地图：行星→星座→宫位→相位的层层递进。）
  3. `核心知识逐层拆解`（主体，50-60%。按知识模块组织：每个模块的核心概念→记忆要点→常见误解→快速理解的类比。）
  4. `从碎片到整合`（500字。如何从"知道每个符号"跃升到"能解读一张完整星盘"。）
  5. `学习路线图`（400字。读完这本书后，下一步学什么？推荐的进阶路径。）
  6. `这本书的局限`（300字。这本书没覆盖什么？哪些地方可能过于简化？）
  7. `延伸阅读`（200字。）

#### 4. 行运与预测
- **文体**：时间技法体
- **语气**：精确但不机械，像一位老练的占星咨询师在解释行运的含义
- **篇幅参考**：7000-10000字
- **必需章节**（7节）：
  1. `时间的语言`（500字。这本书如何理解占星中的"时间"？行运/推运的核心理念。）
  2. `预测框架全景`（600字。全书的预测技法体系：哪些行运最重要？优先级如何？）
  3. `核心技法深度解读`（主体，50-60%。按行星行运/推运技法组织：每种技法的含义→触发条件→典型表现→持续时间→如何有建设性地回应。）
  4. `行运的层次`（500字。外行星行运vs内行星行运的不同层次和意义。）
  5. `实操指南`（500字。如何追踪自己的行运，如何判断哪些行运值得关注。）
  6. `预测的边界`（400字。占星预测能做什么、不能做什么？宿命论vs自由意志。）
  7. `延伸阅读`（200字。）

#### 5. 占星哲学与历史
- **文体**：思想史体
- **语气**：学术但不枯燥，像一位哲学系教授在讲占星学的知识史
- **篇幅参考**：10000-15000字
- **必需章节**（7节）：
  1. `这本书在追问什么`（600字。核心哲学问题：占星学在知识体系中的位置？宇宙与心灵的关系？）
  2. `思想脉络`（700字。全书的论证线索或历史叙事线。）
  3. `核心论证深度解读`（主体，50-60%。按核心论题组织：每个论题的主张→论证过程→证据→反对意见→对占星学理解的影响。）
  4. `思想史坐标`（600字。这本书和哲学史、科学史、占星史的关系。）
  5. `对当代占星实践的意义`（500字。这些哲学/历史洞见如何改变你理解和实践占星的方式？）
  6. `论证的边界`（500字。哪些论证有漏洞？哪些假设需要检验？）
  7. `延伸阅读`（200字。）

#### 6. 神话与原型
- **文体**：神话叙事体
- **语气**：有画面感和仪式感，像一位神话学者在篝火旁讲述天空中的故事
- **篇幅参考**：8000-12000字
- **必需章节**（7节）：
  1. `天空中的故事`（500字。这本书如何将神话与占星连接？核心视角是什么？）
  2. `原型图谱`（600字。全书的核心原型体系：哪些神话对应哪些行星/星座？整体架构。）
  3. `核心原型深度解读`（主体，50-60%。按原型/神话组织：神话故事的核心叙事→对应的占星象征→在个人星盘中的表现→对自我认识的启发。）
  4. `从神话到心理`（500字。这些神话原型如何帮助理解个人心理动力和集体无意识？）
  5. `在星盘中遇见神话`（500字。如何将原型视角应用到实际星盘解读中。）
  6. `这个视角的边界`（400字。原型解读的局限，文化局限性。）
  7. `延伸阅读`（200字。）

**Step 2: Verify**

Run: `grep -c '^## \|^### \|^#### ' ~/.claude/skills/astrology-book-skill/references/type-templates-cn.md`
Expected: 6 major sections with 7 required chapters each

---

### Task 4: Write `references/type-templates-en.md`

**Files:**
- Create: `~/.claude/skills/astrology-book-skill/references/type-templates-en.md`

**Step 1: Write the English templates file**

This file contains 6 English templates, each independently designed for English readers. Each template defines:
- Style
- Tone
- Word count range
- Output structure (sections with descriptions)

The 6 templates are:

#### 1. Psychological Astrology
- **Style:** Depth-psychological exploration
- **Tone:** Insightful and reflective, like a Jungian analyst illuminating the psyche through the birth chart
- **Word count:** 4000-6000 words
- **Required sections** (7):
  1. `What This Book Illuminates` (250 words. Core psychological insight — what unconscious dynamics does this book reveal?)
  2. `Key Concepts` (300 words. The book's core astrological-psychological framework: how concepts relate to each other.)
  3. `Deep Dive: Psychological Dynamics` (Main body, 50-60%. Organized by psychological themes: planetary/sign/house symbolism → corresponding psychodynamics → everyday manifestations → paths toward integration.)
  4. `Dialogue with Jungian Psychology` (300 words. How does this book use or develop Jung's archetypes, shadow, individuation?)
  5. `Reading Your Own Chart` (250 words. Practical guidance for applying the book's concepts to chart interpretation.)
  6. `Limitations and Caveats` (200 words. Honest assessment of the book's boundaries.)
  7. `Further Reading` (100 words.)

#### 2. Evolutionary Astrology
- **Style:** Soul-journey narrative
- **Tone:** Profound without being mystical, like an experienced evolutionary astrologer mapping the soul's path
- **Word count:** 4000-6000 words
- **Required sections** (7):
  1. `The Soul's Question` (250 words. What fundamental question about soul evolution does this book address?)
  2. `The Evolutionary Framework` (300 words. The book's model of soul evolution through the birth chart.)
  3. `Deep Dive: Evolutionary Themes` (Main body, 50-60%. Organized by evolutionary themes: Pluto/Nodes/aspects → soul intention → karmic patterns → breakthrough paths.)
  4. `Among the Schools` (250 words. How evolutionary astrology differs from psychological and traditional astrology.)
  5. `Chart Practice` (250 words. How to apply the book's framework to actual chart reading.)
  6. `The Limits of This Framework` (200 words. Honest discussion of verifiability of "soul" and "past life" concepts.)
  7. `Further Reading` (100 words.)

#### 3. Beginner's Guide
- **Style:** Learning companion
- **Tone:** Clear and encouraging, like a patient astrology teacher guiding you step by step
- **Word count:** 2500-4000 words
- **Required sections** (7):
  1. `What This Book Teaches` (200 words. The book's scope and intended audience.)
  2. `Knowledge Map` (250 words. How the book structures astrological knowledge: planets → signs → houses → aspects.)
  3. `Core Concepts Unpacked` (Main body, 50-60%. Organized by knowledge modules: key concepts → memory aids → common misconceptions → intuitive analogies.)
  4. `From Parts to Whole` (250 words. How to move from knowing symbols to reading a complete chart.)
  5. `Your Learning Path` (200 words. What to study next after this book.)
  6. `What This Book Doesn't Cover` (150 words. Gaps and simplifications.)
  7. `Further Reading` (100 words.)

#### 4. Transits and Prediction
- **Style:** Temporal technique analysis
- **Tone:** Precise but humanistic, like an experienced consulting astrologer explaining the meaning of planetary cycles
- **Word count:** 3500-5000 words
- **Required sections** (7):
  1. `The Language of Time` (250 words. How this book understands astrological timing.)
  2. `The Predictive Framework` (300 words. The book's system: which transits matter most and why.)
  3. `Deep Dive: Key Techniques` (Main body, 50-60%. Organized by transit/progression type: meaning → trigger conditions → typical manifestations → duration → constructive responses.)
  4. `Layers of Transit` (250 words. Outer planet vs. inner planet transits — different levels of meaning.)
  5. `Practical Tracking` (250 words. How to monitor your own transits and prioritize attention.)
  6. `The Boundaries of Prediction` (200 words. What astrology can and cannot predict. Fate vs. free will.)
  7. `Further Reading` (100 words.)

#### 5. Astrological Philosophy and History
- **Style:** Intellectual history
- **Tone:** Scholarly yet engaging, like a philosophy professor lecturing on astrology's place in the history of ideas
- **Word count:** 5000-7500 words
- **Required sections** (7):
  1. `The Question at Stake` (300 words. Core philosophical question: astrology's epistemological status, cosmos-psyche relationship.)
  2. `The Arc of the Argument` (350 words. The book's thesis and how it unfolds.)
  3. `Deep Dive: Core Arguments` (Main body, 50-60%. Organized by thesis: each argument's claim → evidence → reasoning → counterarguments → implications for understanding astrology.)
  4. `Intellectual Coordinates` (300 words. Where this book sits in the history of philosophy, science, and astrology.)
  5. `Implications for Practice` (250 words. How these philosophical/historical insights change your approach to astrology.)
  6. `Gaps and Vulnerabilities` (250 words. Weak points in the argument, untested assumptions.)
  7. `Further Reading` (100 words.)

#### 6. Myth and Archetype
- **Style:** Mythological narrative
- **Tone:** Evocative and layered, like a mythologist revealing the living stories behind planetary symbols
- **Word count:** 4000-6000 words
- **Required sections** (7):
  1. `Stories in the Sky` (250 words. How this book connects myth to astrology. The core perspective.)
  2. `The Archetypal Map` (300 words. The book's system of myth-planet/sign correspondences.)
  3. `Deep Dive: Core Archetypes` (Main body, 50-60%. Organized by archetype/myth: mythic narrative → astrological symbolism → personal chart manifestation → self-knowledge insights.)
  4. `From Myth to Psyche` (250 words. How mythic archetypes illuminate personal psychology and the collective unconscious.)
  5. `Meeting Myths in Your Chart` (250 words. How to apply the archetypal lens to chart reading.)
  6. `The Limits of This Lens` (200 words. Cultural limitations, interpretive boundaries.)
  7. `Further Reading` (100 words.)

**Step 2: Verify**

Run: `grep -c '^## \|^### \|^#### ' ~/.claude/skills/astrology-book-skill/references/type-templates-en.md`
Expected: 6 major sections with 7 required chapters each

---

### Task 5: Write `scripts/validate.sh`

**Files:**
- Create: `~/.claude/skills/astrology-book-skill/scripts/validate.sh`
- Reference: `~/.claude/skills/book-deconstruction-skill/scripts/validate.sh`

**Step 1: Write the validation script**

The script accepts 3 arguments:
```bash
bash validate.sh <中文文件> <英文文件> <占星子类型>
```

Valid types: `心理占星 | 演化占星 | 入门教程 | 行运与预测 | 占星哲学与历史 | 神话与原型`

**Checks to implement (5 categories):**

**一、文件完整性**
- Both files exist
- Chinese naming: `《书名》 - 作者.md`
- English naming: `《Book Title》 - Author.md` (angle brackets)
- Chinese path contains `中文`
- English path contains `英文`

**二、中文版格式检查**
- 无 YAML (no `---` at line 1)
- 无 callouts (no `> [!`)
- 无 mermaid (no ` ```mermaid`)
- 无 wikilinks (no `[[`)
- 无 ==高亮== (no `==text==`)
- 全书速览引用块 (first 20 lines contain `>`)
- 子类型必需章节全部存在
- 字数在类型范围内（15% tolerance → warning, beyond → error）

**三、英文版格式检查**
- Same MD purity checks (no YAML, callouts, mermaid, wikilinks, highlights)
- Opening overview block present
- English subtype required sections all present
- Word count in type range

**四、中文写作规范**
- 10 methodology terms zero leakage
- 无【】brackets
- 第二人称 "你" present
- 无偷懒句式
- 标签式加粗 < 3 consecutive
- 加粗+破折号 < 3 instances
- 编号式加粗 < 2 instances
- 加粗密度 ≤ 5/千字

**五、英文写作规范**
- 10 methodology terms zero leakage (English equivalents: "Feynman", "first principles", "DIKW", "Socratic", "Bloom", "golden circle", "mental model", "antifragile", "analogy transfer", "concept network")
- Bold density ≤ 5 per 1000 words
- No lazy phrases ("as mentioned above", "space constraints", "similarly to above")
- Second person "you" present

**Key implementation details:**

- Reuse `char_count()` from existing script for Chinese character counting
- Add `word_count()` function for English word counting:
```bash
word_count() {
    if [[ ! -f "$1" ]]; then echo "0"; return; fi
    perl -e '
        open my $fh, "<:encoding(UTF-8)", $ARGV[0] or die;
        local $/; my $t = <$fh>; close $fh;
        $t =~ s/\A---\n.*?\n---\n//s;
        $t =~ s/^#+\s*//gm;
        $t =~ s/\*\*//g;
        $t =~ s/^>\s*//gm;
        $t =~ s/```\w*\n.*?```//gs;
        $t =~ s/\[([^\]]*)\]\([^\)]*\)/$1/g;
        $t =~ s/^[-*+]\s+//gm;
        my @words = ($t =~ /[a-zA-Z]+(?:'\''[a-zA-Z]+)*/g);
        print scalar @words;
    ' "$1"
}
```

- Type → section mapping functions for both CN and EN
- Type → word count range functions for both CN and EN

**Step 2: Make executable and test**

Run: `chmod +x ~/.claude/skills/astrology-book-skill/scripts/validate.sh`
Run: `bash ~/.claude/skills/astrology-book-skill/scripts/validate.sh 2>&1 | head -5`
Expected: Usage message showing parameter requirements

---

### Task 6: Write `SKILL.md`

**Files:**
- Create: `~/.claude/skills/astrology-book-skill/SKILL.md`

**Step 1: Write the main skill file**

The SKILL.md has these major sections:

**Frontmatter:**
```yaml
---
name: astrology-book-deconstruction
description: "占星书籍深度拆解系统。当用户请求拆解占星书籍时触发，自动生成中文+英文两份深度拆解文件。支持6种占星子类型（心理占星、演化占星、入门教程、行运与预测、占星哲学与历史、神话与原型）的差异化输出。适用场景：(1)用户说'拆解《占星书名》'；(2)用户上传占星书籍并要求分析；(3)用户要求对占星书进行深度解读。"
---
```

**Core sections to include:**

1. **核心理念** — 一句话概括：本技能生成中英文双语的深度占星书读书笔记。

2. **输出规范**
   - 文件1：中文深度拆解版（路径、格式、特点）
   - 文件2：英文深度拆解版（路径、格式、特点）
   - 明确说明：纯净 Markdown，无 YAML/callouts/wikilinks/高亮

3. **占星子类型识别**（6种类型表格 + 识别特征 + 示例）

4. **工作流**（6 步）
   - Step 1: 识别占星子类型
   - Step 2: 评估复杂度确定篇幅
   - Step 3: 加载中文模板生成中文版（参考 `references/type-templates-cn.md`）
   - Step 4: 加载英文模板生成英文版（参考 `references/type-templates-en.md`，独立写作非翻译）
   - Step 5: 运行验证脚本 + 修复循环（最多3轮）
   - Step 6: 内容质量快检（4项）

5. **核心输出原则**（复用自现有 skill）
   - 方法论完全隐形（含示例对比，用占星场景重写示例）
   - 写作风格（中文版：第二人称、术语附英文；英文版：原创写作、标准术语）
   - 格式净化规则（消除 AI 痕迹）— 全部复用
   - 类型自适应语气表（6种占星子类型各自的中英文语气）

6. **内部质量规则**（复用自现有 skill）
   - 防幻觉
   - 防遗漏
   - 掌握度过低时的处理（中英文各自的声明模板）

7. **验证脚本用法**
   ```bash
   bash ~/.claude/skills/astrology-book-skill/scripts/validate.sh \
     "<中文文件路径>" "<英文文件路径>" "<占星子类型>"
   ```
   - 修复-验证循环说明（最多3轮）
   - 修复策略速查
   - 内容质量快检（4项）
   - 完成标准

8. **参考文件**
   - `references/type-templates-cn.md`
   - `references/type-templates-en.md`
   - `references/methodologies.md`

**Step 2: Verify**

Run: `head -5 ~/.claude/skills/astrology-book-skill/SKILL.md`
Expected: YAML frontmatter with `name: astrology-book-deconstruction`

Run: `wc -l ~/.claude/skills/astrology-book-skill/SKILL.md`
Expected: approximately 400-600 lines

---

### Task 7: Smoke test the complete skill

**Step 1: Verify all files exist**

Run:
```bash
echo "=== File Structure ==="
find ~/.claude/skills/astrology-book-skill -type f | sort

echo "=== Line Counts ==="
wc -l ~/.claude/skills/astrology-book-skill/SKILL.md
wc -l ~/.claude/skills/astrology-book-skill/references/type-templates-cn.md
wc -l ~/.claude/skills/astrology-book-skill/references/type-templates-en.md
wc -l ~/.claude/skills/astrology-book-skill/references/methodologies.md
wc -l ~/.claude/skills/astrology-book-skill/scripts/validate.sh
```

Expected: 5 files, all with substantial content.

**Step 2: Verify validate.sh runs without syntax errors**

Run: `bash ~/.claude/skills/astrology-book-skill/scripts/validate.sh 2>&1 | head -3`
Expected: Usage message (not a bash syntax error)

**Step 3: Verify SKILL.md frontmatter is valid**

Run: `head -4 ~/.claude/skills/astrology-book-skill/SKILL.md`
Expected:
```
---
name: astrology-book-deconstruction
description: "占星书籍深度拆解系统..."
---
```

**Step 4: Verify all 6 Chinese subtypes have templates**

Run: `grep '^## ' ~/.claude/skills/astrology-book-skill/references/type-templates-cn.md`
Expected: 6 section headers for the 6 subtypes

**Step 5: Verify all 6 English subtypes have templates**

Run: `grep '^## ' ~/.claude/skills/astrology-book-skill/references/type-templates-en.md`
Expected: 6 section headers for the 6 subtypes

---

### Task 8: Commit

**Step 1: Stage and commit all files**

```bash
cd /Users/wzb/obsidian
git add .claude/skills/astrology-book-skill/ docs/plans/2026-02-25-astrology-book-skill-design.md docs/plans/2026-02-25-astrology-book-skill-plan.md
git commit -m "feat: add astrology-book-skill for bilingual book deconstruction

New skill for deconstructing astrology books into Chinese + English
deep-analysis notes. Supports 6 subtypes: psychological, evolutionary,
beginner, transits, philosophy/history, myth/archetype."
```
