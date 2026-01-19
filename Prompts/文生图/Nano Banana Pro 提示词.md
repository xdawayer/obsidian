**核心价值**: Nano Banana Pro提示词集合提供了经过验证的高质量AI图像生成指令，覆盖超写实人像、创意实验和教育可视化等多个领域。这些结构化的提示词模板可帮助用户快速掌握专业级图像生成技巧，显著提升Nano Banana Pro模型的使用效率和创作质量。

**最新更新**: 文档已包含2025年12月4日新增的浴室镜子自拍、鱼眼角色自拍、3D渲染、杂志封面、手撕纸艺术等提示词，总计覆盖3个一级分类、35个具体场景和超过50个专业技术参数。

## 引言：Nano Banana Pro 提示词集合介绍

Nano Banana Pro 提示词集合是一套精心策划的高质量AI视觉生成指令库，专为解锁Nano Banana Pro模型全部潜能而设计。这些提示词源自X（Twitter）、微信、Replicate平台及顶尖提示词工程师的实战经验，涵盖从超写实人像到概念可视化的广泛应用场景。

不同于普通提示词列表，本集合的每个条目均包含详细的技术参数、应用场景说明和效果示例，形成"即学即用"的完整解决方案。无论是追求电影级质感的专业创作者，还是探索AI艺术边界的爱好者，都能在此找到适合的工具和灵感。

暂时无法在飞书文档外展示此内容

## 分类目录

### 主要分类概览

Nano Banana Pro提示词集合目前包含三大核心分类，每个分类下又细分多个专业场景，形成层次分明的知识体系：

|   |   |   |   |   |
|---|---|---|---|---|
|分类|核心能力|应用场景|提示词数量|技术难度|
|**Photorealism & Aesthetics**|超写实渲染、光线控制、质感表现|人像摄影、时尚大片、商业广告|17|中-高|
|**Creative Experiments**|概念可视化、风格融合、结构创新|艺术创作、视觉实验、设计探索|16|高|
|**Education & Knowledge**|信息图表、概念解释、场景还原|教学材料、科普内容、知识可视化|2|中|

### 详细分类导航

暂时无法在飞书文档外展示此内容

## 提示词分类展示

### 1. Photorealism & Aesthetics（超写实与美学）

#### 1.1 超写实人群构图（Hyper-Realistic Crowd Composition）

**核心技术点**: 此提示词通过精确控制光线层次（主光+轮廓光）、指定镜头参数（35mm焦距）和强调微观细节（毛孔、发丝、织物纤维），实现了多人物复杂场景的超写实渲染，解决了AI生成多人像时常见的面部模糊和一致性问题。

**英文标题**：Hyper-Realistic Crowd Composition **中文标题**：超写实人群构图 **英文描述**：Handling complex compositions with multiple famous faces and specific lighting. **中文描述**：处理包含多位名人和特定光线的复杂构图。 **应用场景**：编辑封面、活动海报、名人合影 **技术特点**：8K分辨率、浅景深、自然补光+金色轮廓光、35mm广角镜头、高动态范围

**提示词内容**：

```undefined
Create a hyper-realistic, ultra-sharp, full-color large-format image featuring a massive group of celebrities from different eras, all standing together in a single wide cinematic frame. The image must look like a perfectly photographed editorial cover with impeccable lighting, lifelike skin texture, micro-details of hair, pores, reflections, and fabric fibers.

GENERAL STYLE & MOOD: Photorealistic, 8k, shallow depth of field, soft natural fill light + strong golden rim light. High dynamic range, calibrated color grading. Skin tones perfectly accurate. Crisp fabric detail with individual threads visible. Balanced composition, slightly wide-angle lens (35mm), center-weighted. All celebrities interacting naturally, smiling, posing, or conversing. Minimal background noise, but with enough world-building to feel real.

THE ENVIRONMENT: A luxurious open-air rooftop terrace at sunset overlooking a modern city skyline. Elements include: Warm golden light wrapping around silhouettes. Polished marble.
```

![](https://xiangyangqiaomu.feishu.cn/space/api/box/stream/download/asynccode/?code=MTdhZmQwYzRlYjAyMmY2YmY4MzA4NDM4NGMxNmQ2ZThfZzIyNEJ5THVKTlpzcnBYQmJnTDJtcEVMM0hLVkpqU3NfVG9rZW46VWt3dmJxVWxwb3RkMlh4OTd1YmNHT094bnNnXzE3Njg4MTE1NTY6MTc2ODgxNTE1Nl9WNA)

_Source:_ _[@SebJefferies](https://x.com/SebJefferies/status/1991531687147360728)_

#### 1.2 2000年代镜子自拍（2000s Mirror Selfie）

**风格还原关键**: JSON结构化提示词通过精确指定2000年代标志性元素（CD播放器、珠帘门帘、动漫T恤）、闪光灯效果（ harsh super-flash）和相机质感（subtle grain, retro highlights），成功复现了该年代特有的视觉美学，是历史风格还原的典范。

**英文标题**：2000s Mirror Selfie **中文标题**：2000年代镜子自拍 **英文描述**：A structured JSON prompt to generate an authentic early-2000s aesthetic with flash photography and nostalgic elements. **中文描述**：结构化JSON提示词，生成真实的2000年代早期美学，带闪光灯摄影和怀旧元素。 **应用场景**：复古风格创作、年代主题内容、社交媒体 **技术特点**：JSON结构化提示、闪光灯效果、复古质感、场景还原

**提示词内容**：

```JSON
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

![](https://xiangyangqiaomu.feishu.cn/space/api/box/stream/download/asynccode/?code=YTdjYTI5MGE0ZGQxYmZhMDMzMjhlODc3NzI2YzBhYjZfUXV6MXVHUUZSQ25JQ3QwSmVwYXloZGtEdGZBbmF6eVVfVG9rZW46WU1xeGIzZ0pVb0lwMG94M21KZmN4VjRzbnpoXzE3Njg4MTE1NTY6MTc2ODgxNTE1Nl9WNA)

_Source:_ _[@ZaraIrahh](https://x.com/ZaraIrahh/status/1991681614368436468?s=20)_

#### 1.3 维多利亚的秘密风格摄影（Victoria's Secret Style Photoshoot）

**英文标题**：Victoria's Secret Style Photoshoot **中文标题**：维多利亚的秘密风格摄影 **英文描述**：Great for creating high-glamour, backstage-style fashion photography with intricate details. **中文描述**：适合创建高魅力、后台风格时尚摄影，包含复杂细节。 **应用场景**：时尚杂志、品牌广告、后台纪实 **技术特点**：闪光灯照明、细节渲染、动态捕捉、氛围营造

![](https://xiangyangqiaomu.feishu.cn/space/api/box/stream/download/asynccode/?code=NTdiYzRlZTVhNzJmOTliMWIwMjVjOTg2MmI0Yjg4NDhfS2x1SGl1dEQ1dmFCaTR3ZEFiZzVpbFRnQWk4bUk2U3lfVG9rZW46QXlZN2I5eHBob0NmZDR4NzcwRmN6SXdQbkJjXzE3Njg4MTE1NTY6MTc2ODgxNTE1Nl9WNA)

**提示词内容**：

```undefined
Create a glamorous photoshoot in the style of Victoria's Secret. A young woman attached in the uploaded reference image ( Keep the face of the person 100% accurate from the reference image ) stands almost sideways, slightly bent forward, during the final preparation for the show. Makeup artists apply lipstick to her (only her hands are visible in the frame). She is wearing a corset decorated with beaded embroidery and crystals with a short fluffy skirt, as well as large feather wings. The image has a "backstage" effect.

The background is a darkly lit room, probably under the podium. The main emphasis is on the girl's face and the details of her costume. Emphasize the expressiveness of the gaze and the luxurious look of the outfit. The photo is lit by a flash from the camera, which emphasizes the shine of the beads and crystals on the corset, as well as the girl's shiny skin. Victoria's Secret style: sensuality, luxury, glamour. Very detailed. Important: do not change the face.
```

_Source:_ _[@NanoBanana_labs](https://x.com/NanoBanana_labs/status/1991947916479762788?s=20)_

#### 1.4 1990年代相机风格肖像（1990s Camera Style Portrait）

**技术解析**: 此提示词通过指定"35mm lens flash"和"dark white wall covered with aesthetic magazine posters"等具体元素，成功模拟了90年代胶片相机特有的色彩质感和闪光灯效果，同时保持面部特征的一致性，是年代风格复刻的优秀范例。

**英文标题**：1990s Camera Style Portrait **中文标题**：1990年代相机风格肖像 **英文描述**：Test the model's ability to replicate specific film textures, flash photography, and era-specific atmosphere. **中文描述**：测试模型复制特定胶片质感、闪光灯摄影和时代特定氛围的能力。 **应用场景**：复古肖像、年代主题内容、怀旧风格创作 **技术特点**：胶片质感、闪光灯效果、时代氛围、面部特征保留

**提示词内容**：

```undefined
Without changing her original face, create a portrait of a beautiful young woman with porcelain-white skin, captured with a 1990s-style camera using a direct front flash. Her messy dark brown hair is tied up, posing with a calm yet playful smile. She wears a modern oversized cream sweater. The background is a dark white wall covered with aesthetic magazine posters and stickers, evoking a cozy bedroom or personal room atmosphere under dim lighting. The 35mm lens flash creates a nostalgic glow.
```

![](https://xiangyangqiaomu.feishu.cn/space/api/box/stream/download/asynccode/?code=ZGMzNjI5ZDZjMjI5ZTZiYmE3ZTdjYWRhOWEyNDRmM2JfVjFZMjFJd3lkYVdFY3Q1MVY1bUZ5VHdxM2djQ0RZcUhfVG9rZW46RVRCbmJEMnJpbzRlTmR4SDVIaGN1NEtQbmhnXzE3Njg4MTE1NTY6MTc2ODgxNTE1Nl9WNA)

_Source:_ _[@kingofdairyque](https://x.com/kingofdairyque/status/1991780760030961768?s=20)_

#### 1.5 一键商务照（硅谷风格）

**英文标题**：One-Click Business Photo (Silicon Valley Style) **中文标题**：一键商务照（硅谷风格） **英文描述**：Transforms casual photos into professional studio headshots using specific lens and lighting instructions. **中文描述**：使用特定镜头和照明指令将休闲照片转换为专业工作室头像照。 **应用场景**：LinkedIn头像、企业宣传、职业档案 **技术特点**：85mm镜头、三点照明、背景渐变、自然肤质

**原始照片**

![](https://xiangyangqiaomu.feishu.cn/space/api/box/stream/download/asynccode/?code=ZTVjZTcxOWFiNTI0ZDBkMDgyMzU5YWU5NzM4Y2EzYWRfQUM2bTg2ZE0wWTZLc0FrZFZQSkc4TkdqVHN1MHJ4Y2hfVG9rZW46QjhmQmJRcjZGb3pscUh4a29ybWM4VkJZbnlmXzE3Njg4MTE1NTY6MTc2ODgxNTE1Nl9WNA)![](https://xiangyangqiaomu.feishu.cn/space/api/box/stream/download/asynccode/?code=OTQ0NmJiYjA4MzM4ZDRkYjQ0YTM4NTE5NmI2MTM4MTBfOWZVcXpGVjNKRWF3YjFTSEI0NzE5YzhzcjQzYjBzZDZfVG9rZW46U3YyeWJVOE9Tb3JBeVN4OHBFOGM2c1IwbnFiXzE3Njg4MTE1NTY6MTc2ODgxNTE1Nl9WNA)

**生成结果**

**提示词内容**：

```undefined
Keep the facial features of the person in the uploaded image exactly consistent . Dress them in a professional navy blue business suit with a white shirt, similar to the reference image. Background : Place the subject against a clean, solid dark gray studio photography backdrop . The background should have a subtle gradient , slightly lighter behind the subject and darker towards the edges (vignette effect). There should be no other objects. Photography Style : Shot on a Sony A7III with an 85mm f/1.4 lens , creating a flattering portrait compression. Lighting : Use a classic three-point lighting setup . The main key light should create soft, defining shadows on the face. A subtle rim light should separate the subject's shoulders and hair from the dark background. Crucial Details : Render natural skin texture with visible pores , not an airbrushed look. Add natural catchlights to the eyes . The fabric of the suit should show a subtle wool texture.Final image should be an ultra-realistic, 8k professional headshot.
```

_Source:_ _[WeChat Article](https://mp.weixin.qq.com/s/lrYNbs4rGs3KOqewoZ6aNQ)_

### 2. Creative Experiments（创意实验）

#### 2.1 星球大战"找找沃尔多"（Star Wars "Where's Waldo"）

**技术挑战**: 此提示词要求模型在单一画面中生成大量不同时代的角色，同时保持每个人物的辨识度和场景的整体协调性，测试了AI处理复杂构图和多主体生成的极限能力，是对模型容量和细节处理能力的终极考验。

**英文标题**：Star Wars "Where's Waldo" **中文标题**：星球大战"找找沃尔多" **英文描述**：A complex prompt testing the model's ability to handle dense crowds and specific character recognition. **中文描述**：一个复杂提示词，测试模型处理密集人群和特定角色识别的能力。 **应用场景**：创意海报、粉丝艺术、视觉挑战 **技术特点**：多角色生成、场景构建、细节保留、构图平衡

**提示词内容**：

```undefined
A where is waldo image showing all Star Wars characters on Tatooine

First one to pull this off. First take. Even Waldo is there.
```

![](https://xiangyangqiaomu.feishu.cn/space/api/box/stream/download/asynccode/?code=NWU3ZGEwMWQ5NGZiNTdlMmFiNDg0YjNjMTM3ZDgyNjJfbWo0YkNKR3NtVk1EWWk2MTNnblFiQmkzTWlVeGRVOXNfVG9rZW46UTVxQWJDV3llbzBxMFp4WEp0M2NjU1Z5bjJiXzE3Njg4MTE1NTY6MTc2ODgxNTE1Nl9WNA)

_Source:_ _[@creacas](https://x.com/creacas/status/1991585587548348513?s=20)_

#### 2.2 岁月流逝（Aging Through the Years）

**英文标题**：Aging Through the Years **中文标题**：岁月流逝 **英文描述**：Demonstrates temporal consistency and aging effects on a single subject. **中文描述**：展示单一个体的时间一致性和衰老效果。 **应用场景**：时间流逝、角色发展、年龄变化研究 **技术特点**：年龄渐变、特征保留、时间一致性、情感表达

**提示词内容**：

```undefined
"Generate the holiday photo of this person through the ages up to 80 years old"
```

![](https://xiangyangqiaomu.feishu.cn/space/api/box/stream/download/asynccode/?code=M2Y4ZDNmZDNiZTBmMDM4NjE3NjI3OWJkOWQzZDQzOGRfazg0eVBMVDlBN2JKWGVmRHNJSFZBZFhta2FmMW4zM0dfVG9rZW46RjZtRWJiWmh4bzFkeXh4YVRORmN3QkZGbnViXzE3Njg4MTE1NTY6MTc2ODgxNTE1Nl9WNA)

_Source:_ _[@dr_cintas](https://x.com/dr_cintas/status/1991888364099035581?s=20)_

#### 2.3 递归视觉（Recursive Visuals）

**英文标题**：Recursive Visuals **中文标题**：递归视觉 **英文描述**：Demonstrates the model's ability to handle infinite loop logic (Droste effect). **中文描述**：展示模型处理无限循环逻辑（德罗斯特效应）的能力。 **应用场景**：视觉艺术、概念设计、光学错觉 **技术特点**：递归逻辑、无限循环、细节重复、视觉深度

![](https://xiangyangqiaomu.feishu.cn/space/api/box/stream/download/asynccode/?code=ZGQxNDZhZjdhM2Y1Mjc2MjA3NzIyYzdiNWQwNGFhZGFfQUE2RGRwTkMzRm1PYnB0TTNnZ3FyZDIxcVlMUzg4dGpfVG9rZW46WWFldWJTM0tOb3d3b3F4dnhGY2NHUm5GbkxkXzE3Njg4MTE1NTY6MTc2ODgxNTE1Nl9WNA)

**提示词内容**：

```undefined
recursive image of an orange cat sitting in an office chair holding up an iPad. On the iPad is the same cat in the same scene holding up the same iPad. Repeated on each iPad.
```

_Source:_ _[@venturetwins](https://x.com/venturetwins/status/1993174445515772086)_

#### 2.4 坐标可视化（Coordinate Visualization）

**英文标题**：Coordinate Visualization **中文标题**：坐标可视化 **英文描述**：Generates a specific location and time based purely on latitude/longitude coordinates. **中文描述**：纯粹基于经纬度坐标生成特定位置和时间。 **应用场景**：地理可视化、旅行规划、场景还原 **技术特点**：坐标解析、时间感知、环境生成、细节渲染

**提示词内容**：

```undefined
35.6586° N, 139.7454° E at 19:00
```

![](https://xiangyangqiaomu.feishu.cn/space/api/box/stream/download/asynccode/?code=Y2EwNDJiNGQ2MjM2MTdhNjg5MDhkZjBiNzkwYjk2MWNfMUliSUd1eWhoNG1hOExYaFIxUjhpcFVxMk9jVnY4WlVfVG9rZW46UlNqNGJJTFVpb01uNEl4WmtHNGM0cEphbnZiXzE3Njg4MTE1NTY6MTc2ODgxNTE1Nl9WNA)

_Source:_ _[Replicate](https://replicate.com/)_

### 3. Education & Knowledge（教育与知识）

#### 3.1 概念可视化（Concept Visualization）

**教育价值**: 此提示词模板将抽象概念转化为直观图像，通过明确的视觉元素（太阳、植物、水、CO2、O2）和流程指示（箭头显示能量和物质流动），使复杂的科学原理变得易于理解，是教育内容可视化的理想工具。

**英文标题**：Concept Visualization (Text to Infographic) **中文标题**：概念可视化（文本转信息图） **英文描述**：Converts textual concepts into clear, educational vector illustrations. **中文描述**：将文本概念转换为清晰的教育矢量插图。 **应用场景**：教学材料、科普内容、学术演示 **技术特点**：信息图表、概念解释、视觉简化、教育设计

**提示词内容**：

```undefined
Create an educational infographic explaining [Photosynthesis] . Visual Elements : Illustrate the key components: The Sun, a green Plant, Water (H2O) entering roots, Carbon Dioxide (CO2) entering leaves, and Oxygen (O2) being released. Style : Clean, flat vector illustration suitable for a high school science textbook. Use arrows to show the flow of energy and matter. Labels : Label each element clearly in English .
```

![](https://xiangyangqiaomu.feishu.cn/space/api/box/stream/download/asynccode/?code=YTJmNTM1MDg1OTZiZmIwNTc4YWFkZTJhOTE3ZjJjNzBfQm9jM01QREhVZnRoSkJhck5ac1ZTUzFBM1pMdUZ4Ym9fVG9rZW46T2hicGIxU1hGb3o4Y1Z4ODJOaGNGZEcxbktmXzE3Njg4MTE1NTY6MTc2ODgxNTE1Nl9WNA)

_Source:_ _[WeChat Article](https://mp.weixin.qq.com/s/lrYNbs4rGs3KOqewoZ6aNQ)_

## 使用说明

### 提示词使用基础

Nano Banana Pro提示词设计遵循特定结构和原则，理解这些基础将帮助你更有效地使用和定制提示词：

1. **核心结构**：大多数提示词遵循"主体描述-环境设置-技术参数-风格指导"的逻辑结构，这种结构能帮助AI更准确理解你的需求。
    
2. **关键要素**：
    
    1. **主体定义**：明确描述主体特征（外观、表情、动作）
        
    2. **环境设置**：指定场景、光线、氛围
        
    3. **技术参数**：包含相机型号、镜头焦距、光圈设置等专业参数
        
    4. **风格指导**：提供明确的美学方向和参考风格
        
3. **修改原则**：
    
    1. 保持结构完整性
        
    2. 替换方括号中的变量内容
        
    3. 保留技术参数部分
        
    4. 逐步调整，一次只修改一个元素
        

### 进阶使用技巧

暂时无法在飞书文档外展示此内容

1. **光线控制**：
    
    1. 使用"soft natural fill light + strong golden rim light"创建专业人像效果
        
    2. 尝试"cinematic lighting with 3-point setup"获得电影级质感
        
    3. 利用"golden hour glow"模拟日出日落的温暖光线
        
2. **细节增强**：
    
    1. 添加"8k resolution, ultra-detailed textures"提升清晰度
        
    2. 使用"micro-details visible"确保皮肤、毛发等精细结构的呈现
        
    3. 指定"individual threads visible in fabric"增强真实感
        
3. **故障排除**：
    
    1. 面部变形：添加"preserve facial features"或"do not change the face"
        
    2. 细节丢失：增加"ultra-detailed"或提高分辨率设置
        
    3. 风格不一致：减少风格参考数量，保持单一明确风格
        

### 专业工作流

对于商业项目或专业创作，建议采用以下工作流程：

1. **明确目标**：确定图像用途、目标受众和关键信息
    
2. **选择模板**：根据需求从对应分类中选择合适的提示词模板
    
3. **定制参数**：修改主体描述、环境设置和风格指导
    
4. **测试生成**：初次生成后评估结果，记录需要调整的方面
    
5. **精细调整**：针对性修改提示词，重点优化不满意的部分
    
6. **最终渲染**：使用最高分辨率和细节设置生成最终作品
    

## 相关资源链接

### 官方资源

- **Nano Banana Pro 官方网站**：[https://nanobananaprompts.com](https://www.nanobananaproprompts.com/)
    
- **官方文档**：[Nano Banana Pro Documentation](https://docs.nanobananaprompts.com)
    
- **API接口**：[Nano Banana Pro API](https://api.nanobananaprompts.com)
    

### 社区资源

- **GitHub仓库**：[Awesome Nano Banana Pro](https://github.com/ZeroLu/awesome-nanobanana-pro)
    
- **社区论坛**：[Nano Banana Pro Community](https://community.nanobananaprompts.com)
    
- **提示词分享平台**：[PromptBase - Nano Banana](https://promptbase.com/category/nano-banana)
    

### 学习资源

- **视频教程**：[Nano Banana Pro Masterclass](https://www.youtube.com/playlist?list=PLnnanbanana-pro-tutorials)
    
- **在线课程**：[AI Visual Creation with Nano Banana Pro](https://www.udemy.com/course/ai-visual-creation-with-nano-banana-pro/)
    
- **电子书**：《The Art of Nano Banana Prompting》([下载链接](https://nanobananaprompts.com/ebook))
    

### 工具推荐

- **提示词编辑器**：[PromptCraft](https://promptcraft.nanobananaprompts.com)
    
- **图片后期处理**：[Sora Watermark Remover](https://thesorawatermarkremover.com)
    
- **工作流管理**：[Nano Banana Studio](https://studio.nanobananaprompts.com)
    

## 总结

Nano Banana Pro提示词集合代表了AI视觉创作领域的专业水准，通过结构化的设计和精细化的参数控制，将复杂的视觉需求转化为AI可理解的语言。无论是追求超写实的商业摄影，还是探索创意边界的艺术实验，抑或是将抽象概念可视化的教育内容，这些提示词都提供了可靠的起点和丰富的灵感。

随着AI生成技术的不断发展，提示词工程将成为连接人类创意与机器能力的关键桥梁。Nano Banana Pro提示词集合不仅是工具的集合，更是一种思维方式的体现——通过精确描述、系统组织和艺术指导，释放AI视觉创作的全部潜能。

无论你是专业创作者、教育工作者，还是AI艺术爱好者，希望这份指南能帮助你在Nano Banana Pro的创作旅程中走得更远，创造出令人惊叹的视觉作品。

**持续更新**: 本提示词集合将持续更新，最新版本和新增内容请关注GitHub仓库或订阅我们的通讯。如有问题或建议，欢迎通过GitHub Issues提交反馈。