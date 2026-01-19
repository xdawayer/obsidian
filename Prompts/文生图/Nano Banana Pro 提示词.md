---
title: "Nano Banana Pro 提示词"
date: "2026-01-19"
tags:
  - prompt
  - image_generation
  - nano_banana_pro
  - ai_art
  - photorealism
category: Prompts/文生图
status: active
description: 包含超写实人像、创意实验和教育可视化等多个领域的 Nano Banana Pro 高质量提示词集合。
---

# Nano Banana Pro 提示词集合

> [!ABSTRACT] 核心价值
> Nano Banana Pro提示词集合提供了经过验证的高质量AI图像生成指令，覆盖超写实人像、创意实验和教育可视化等多个领域。
> 这些结构化的提示词模板可帮助用户快速掌握专业级图像生成技巧，显著提升 Nano Banana Pro 模型的使用效率和创作质量。

> [!INFO] 更新日志
> **最新更新**: 2025年12月4日
> **新增内容**: 浴室镜子自拍、鱼眼角色自拍、3D渲染、杂志封面、手撕纸艺术等。
> **覆盖范围**: 3个一级分类、35个具体场景、>50个专业技术参数。

## 📖 引言

Nano Banana Pro 提示词集合是一套精心策划的高质量AI视觉生成指令库。源自 X (Twitter)、Replicate 平台及顶尖提示词工程师实战经验。
每个条目均包含详细的技术参数、应用场景说明和效果示例，形成"即学即用"的完整解决方案。

## 📂 分类目录

### 主要分类概览

| 分类 | 核心能力 | 应用场景 | 数量 | 难度 |
| :--- | :--- | :--- | :--- | :--- |
| **Photorealism & Aesthetics** | 超写实渲染、光线控制、质感表现 | 人像摄影、时尚大片、商业广告 | 17 | 中-高 |
| **Creative Experiments** | 概念可视化、风格融合、结构创新 | 艺术创作、视觉实验、设计探索 | 16 | 高 |
| **Education & Knowledge** | 信息图表、概念解释、场景还原 | 教学材料、科普内容、知识可视化 | 2 | 中 |

---

## 🎨 提示词分类展示

### 1. Photorealism & Aesthetics (超写实与美学)

#### 1.1 超写实人群构图 (Hyper-Realistic Crowd Composition)

> [!TIP] 核心技术点
> 精确控制光线层次（主光+轮廓光）、指定镜头参数（35mm焦距）、强调微观细节（毛孔、发丝）。解决多人像面部模糊问题。

- **应用场景**：编辑封面、活动海报、名人合影
- **技术特点**：8K分辨率、浅景深、自然补光+金色轮廓光、35mm广角、HDR

```markdown
Create a hyper-realistic, ultra-sharp, full-color large-format image featuring a massive group of celebrities from different eras, all standing together in a single wide cinematic frame. The image must look like a perfectly photographed editorial cover with impeccable lighting, lifelike skin texture, micro-details of hair, pores, reflections, and fabric fibers.

GENERAL STYLE & MOOD: Photorealistic, 8k, shallow depth of field, soft natural fill light + strong golden rim light. High dynamic range, calibrated color grading. Skin tones perfectly accurate. Crisp fabric detail with individual threads visible. Balanced composition, slightly wide-angle lens (35mm), center-weighted. All celebrities interacting naturally, smiling, posing, or conversing. Minimal background noise, but with enough world-building to feel real.

THE ENVIRONMENT: A luxurious open-air rooftop terrace at sunset overlooking a modern city skyline. Elements include: Warm golden light wrapping around silhouettes. Polished marble.
```

#### 1.2 2000年代镜子自拍 (2000s Mirror Selfie)

> [!TIP] 风格还原关键
> JSON结构化提示词。指定标志性元素（CD播放器、珠帘）、闪光灯效果（harsh super-flash）、相机质感（subtle grain）。

- **应用场景**：复古创作、年代主题
- **技术特点**：JSON结构、闪光灯、复古质感

```json
{
  "subject": {
    "description": "A young woman taking a mirror selfie with very long voluminous dark waves and soft wispy bangs",
    "age": "young adult",
    "expression": "confident and slightly playful",
    "hair": {
      "color": "dark",
      "style": "very long, voluminous waves with soft wispy bangs"
    },
    "clothing": {
      "top": {
        "type": "fitted cropped t-shirt",
        "color": "cream white",
        "details": "features a large cute anime-style cat face graphic with big blue eyes, whiskers, and a small pink mouth"
      }
    },
    "face": {
      "preserve_original": true,
      "makeup": "natural glam makeup with soft pink dewy blush and glossy red pouty lips"
    }
  },
  "accessories": {
    "earrings": {
      "type": "gold geometric hoop earrings"
    },
    "jewelry": {
      "waistchain": "silver waistchain"
    },
    "device": {
      "type": "smartphone",
      "details": "patterned case"
    }
  },
  "photography": {
    "camera_style": "early-2000s digital camera aesthetic",
    "lighting": "harsh super-flash with bright blown-out highlights but subject still visible",
    "angle": "mirror selfie",
    "shot_type": "tight selfie composition",
    "texture": "subtle grain, retro highlights, V6 realism, crisp details, soft shadows"
  },
  "background": {
    "setting": "nostalgic early-2000s bedroom",
    "wall_color": "pastel tones",
    "elements": [
      "chunky wooden dresser",
      "CD player",
      "posters of 2000s pop icons",
      "hanging beaded door curtain",
      "cluttered vanity with lip glosses"
    ],
    "atmosphere": "authentic 2000s nostalgic vibe",
    "lighting": "retro"
  }
}
```

#### 1.3 维多利亚的秘密风格摄影 (Victoria's Secret Style)

- **应用场景**：时尚杂志、品牌广告、后台纪实
- **技术特点**：闪光灯照明、细节渲染、动态捕捉

```markdown
Create a glamorous photoshoot in the style of Victoria's Secret. A young woman attached in the uploaded reference image ( Keep the face of the person 100% accurate from the reference image ) stands almost sideways, slightly bent forward, during the final preparation for the show. Makeup artists apply lipstick to her (only her hands are visible in the frame). She is wearing a corset decorated with beaded embroidery and crystals with a short fluffy skirt, as well as large feather wings. The image has a "backstage" effect.

The background is a darkly lit room, probably under the podium. The main emphasis is on the girl's face and the details of her costume. Emphasize the expressiveness of the gaze and the luxurious look of the outfit. The photo is lit by a flash from the camera, which emphasizes the shine of the beads and crystals on the corset, as well as the girl's shiny skin. Victoria's Secret style: sensuality, luxury, glamour. Very detailed. Important: do not change the face.
```

#### 1.4 1990年代相机风格肖像 (1990s Camera Style Portrait)

> [!TIP] 技术解析
> 指定 "35mm lens flash" 和 "dark white wall covered with aesthetic magazine posters"，模拟90年代胶片色彩质感。

- **应用场景**：复古肖像、怀旧风格
- **技术特点**：胶片质感、闪光灯、时代氛围

```markdown
Without changing her original face, create a portrait of a beautiful young woman with porcelain-white skin, captured with a 1990s-style camera using a direct front flash. Her messy dark brown hair is tied up, posing with a calm yet playful smile. She wears a modern oversized cream sweater. The background is a dark white wall covered with aesthetic magazine posters and stickers, evoking a cozy bedroom or personal room atmosphere under dim lighting. The 35mm lens flash creates a nostalgic glow.
```

#### 1.5 一键商务照 (One-Click Business Photo)

- **应用场景**：LinkedIn头像、职业档案
- **技术特点**：85mm镜头、三点照明、自然肤质

```markdown
Keep the facial features of the person in the uploaded image exactly consistent . Dress them in a professional navy blue business suit with a white shirt, similar to the reference image. Background : Place the subject against a clean, solid dark gray studio photography backdrop . The background should have a subtle gradient , slightly lighter behind the subject and darker towards the edges (vignette effect). There should be no other objects. Photography Style : Shot on a Sony A7III with an 85mm f/1.4 lens , creating a flattering portrait compression. Lighting : Use a classic three-point lighting setup . The main key light should create soft, defining shadows on the face. A subtle rim light should separate the subject's shoulders and hair from the dark background. Crucial Details : Render natural skin texture with visible pores , not an airbrushed look. Add natural catchlights to the eyes . The fabric of the suit should show a subtle wool texture.Final image should be an ultra-realistic, 8k professional headshot.
```

### 2. Creative Experiments (创意实验)

#### 2.1 星球大战"找找沃尔多" (Star Wars "Where's Waldo")

> [!TIP] 技术挑战
> 测试模型处理复杂构图、多主体生成、角色辨识度的极限能力。

- **应用场景**：创意海报、视觉挑战
- **技术特点**：多角色生成、构图平衡

```markdown
A where is waldo image showing all Star Wars characters on Tatooine

First one to pull this off. First take. Even Waldo is there.
```

#### 2.2 岁月流逝 (Aging Through the Years)

- **应用场景**：时间流逝、角色发展
- **技术特点**：年龄渐变、特征保留

```markdown
"Generate the holiday photo of this person through the ages up to 80 years old"
```

#### 2.3 递归视觉 (Recursive Visuals)

- **应用场景**：视觉艺术、光学错觉
- **技术特点**：递归逻辑、无限循环 (德罗斯特效应)

```markdown
recursive image of an orange cat sitting in an office chair holding up an iPad. On the iPad is the same cat in the same scene holding up the same iPad. Repeated on each iPad.
```

#### 2.4 坐标可视化 (Coordinate Visualization)

- **应用场景**：地理可视化、旅行规划
- **技术特点**：坐标解析、时间感知

```markdown
35.6586° N, 139.7454° E at 19:00
```

### 3. Education & Knowledge (教育与知识)

#### 3.1 概念可视化 (Concept Visualization)

> [!TIP] 教育价值
> 将抽象概念转化为直观图像，明确视觉元素和流程指示。

- **应用场景**：教学材料、科普
- **技术特点**：信息图表、视觉简化

```markdown
Create an educational infographic explaining [Photosynthesis] . Visual Elements : Illustrate the key components: The Sun, a green Plant, Water (H2O) entering roots, Carbon Dioxide (CO2) entering leaves, and Oxygen (O2) being released. Style : Clean, flat vector illustration suitable for a high school science textbook. Use arrows to show the flow of energy and matter. Labels : Label each element clearly in English .
```

---

## 🛠️ 使用说明

### 提示词使用基础

1.  **核心结构**：`主体描述` -> `环境设置` -> `技术参数` -> `风格指导`
2.  **关键要素**：
    *   **主体**：外观、表情、动作。
    *   **环境**：场景、光线、氛围。
    *   **参数**：相机型号、焦距、光圈。
    *   **风格**：美学方向、参考风格。
3.  **修改原则**：保持结构完整，替换变量内容，一次修改一个元素。

### 进阶使用技巧

> [!example] 光线控制
> *   `soft natural fill light + strong golden rim light`: 专业人像
> *   `cinematic lighting with 3-point setup`: 电影质感
> *   `golden hour glow`: 温暖光线

> [!example] 细节增强
> *   `8k resolution, ultra-detailed textures`
> *   `micro-details visible` (皮肤、毛发)
> *   `individual threads visible in fabric`

> [!warning] 故障排除
> *   **面部变形**: 添加 `preserve facial features` 或 `do not change the face`
> *   **细节丢失**: 增加 `ultra-detailed` 或提高分辨率
> *   **风格不一致**: 减少风格参考数量

### 专业工作流

1.  **明确目标**：确定用途和受众。
2.  **选择模板**：选择合适分类的提示词。
3.  **定制参数**：修改主体和环境。
4.  **测试生成**：初次评估。
5.  **精细调整**：优化不足之处。
6.  **最终渲染**：最高分辨率输出。

---

## 🔗 相关资源

| 类别 | 资源名称 | 链接 |
| :--- | :--- | :--- |
| **官方** | Nano Banana Pro 官网 | [nanobananaprompts.com](https://nanobananaprompts.com/) |
| | 官方文档 | [docs](https://docs.nanobananaprompts.com) |
| | API 接口 | [API](https://api.nanobananaprompts.com) |
| **社区** | GitHub 仓库 | [Awesome Nano Banana Pro](https://github.com/ZeroLu/awesome-nanobanana-pro) |
| | 社区论坛 | [Community](https://community.nanobananaprompts.com) |
| | PromptBase | [PromptBase](https://promptbase.com/category/nano-banana) |
| **学习** | 视频教程 | [YouTube Playlist](https://www.youtube.com/playlist?list=PLnnanbanana-pro-tutorials) |
| | 在线课程 | [Udemy](https://www.udemy.com/course/ai-visual-creation-with-nano-banana-pro/) |
| | 电子书 | [The Art of Nano Banana Prompting](https://nanobananaprompts.com/ebook) |
| **工具** | 提示词编辑器 | [PromptCraft](https://promptcraft.nanobananaprompts.com) |
| | 去水印 | [Sora Watermark Remover](https://thesorawatermarkremover.com) |
| | 工作流管理 | [Nano Banana Studio](https://studio.nanobananaprompts.com) |
