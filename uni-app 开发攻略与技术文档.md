# uni-app 开发攻略与技术文档

> 基于 uni-app 官方文档（uniapp.dcloud.net.cn）整理，涵盖从入门到进阶的完整开发指南。

---

## 一、框架概述

### 1.1 什么是 uni-app

uni-app 是 DCloud 推出的基于 Vue.js 的跨平台前端应用框架，开发者编写一套代码，可编译发布到 **15+ 个平台**：

| 平台类型 | 支持列表 |
|---------|---------|
| 原生 App | iOS、Android、HarmonyOS Next |
| Web | H5（响应式） |
| 微信生态 | 微信小程序 |
| 支付宝生态 | 支付宝小程序 |
| 字节生态 | 抖音小程序、飞书小程序 |
| 百度生态 | 百度小程序 |
| 其他小程序 | QQ、快手、京东、小红书、钉钉 |
| 快应用 | 华为等厂商快应用 |

### 1.2 核心优势

1. **开发者生态庞大** — 900 万开发者，数百万应用，月活 120 亿
2. **跨平台不牺牲性能** — App 端支持原生渲染，小程序端深度优化
3. **条件编译** — 可针对特定平台编写差异化代码，不丢失平台特有能力
4. **Vue 语法** — 学习成本低，前端开发者可快速上手
5. **丰富插件市场** — 数千款插件可直接使用，支持 NPM 生态
6. **HBuilderX 高效开发** — 官方 IDE，开发效率倍增

### 1.3 技术架构

```
┌─────────────────────────────────────────────┐
│                 uni-app 源代码                │
│          (.vue 单文件组件 + JS/TS)            │
└────────────────────┬────────────────────────┘
                     │  编译器
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌─────────┐ ┌──────────┐ ┌──────────────┐
   │  Web/H5  │ │ 小程序代码 │ │ App 原生渲染  │
   │ (Vue SPA)│ │ (WXML等) │ │ (Webview/原生)│
   └─────────┘ └──────────┘ └──────────────┘
```

**两大核心模块：**

- **编译器**（运行在开发环境）：将 `.vue` 文件编译为各平台特定代码。Vue2 基于 webpack，Vue3 基于 Vite。
- **运行时**（运行在终端设备）：包含基础框架、内置组件和 API 封装，为各平台提供统一开发接口。

---

## 二、环境搭建

### 2.1 方式一：HBuilderX 可视化创建（推荐新手）

1. 下载 HBuilderX：https://www.dcloud.io/hbuilderx.html
2. 菜单 → 文件 → 新建 → 项目
3. 选择 uni-app 模板，填写项目名称
4. 点击创建

**特点：** 代码在项目根目录，编译器内置在 HBuilderX 中，产出位于 `unpackage/` 目录。

### 2.2 方式二：CLI 命令行创建（推荐工程化团队）

**环境要求：** Node.js 18+ 或 20+

```bash
# Vue 3 + JavaScript
npx degit dcloudio/uni-preset-vue#vite my-vue3-project

# Vue 3 + TypeScript
npx degit dcloudio/uni-preset-vue#vite-ts my-vue3-project

# Vue 2（需先全局安装 @vue/cli）
npm install -g @vue/cli
vue create -p dcloudio/uni-preset-vue my-project
```

**特点：** 代码在 `src/` 目录，编译器在项目 node_modules 中，产出在 `dist/` 目录。可使用任意 IDE 开发。

### 2.3 运行与发布命令

```bash
# 开发模式
npm run dev:h5          # Web
npm run dev:mp-weixin   # 微信小程序
npm run dev:mp-alipay   # 支付宝小程序
npm run dev:mp-toutiao  # 抖音小程序
npm run dev:app         # App

# 生产构建
npm run build:h5
npm run build:mp-weixin
npm run build:mp-alipay
npm run build:app
```

---

## 三、项目结构

### 3.1 标准目录结构

```
├── pages/                  # 页面文件目录
│   ├── index/
│   │   └── index.vue       # 首页
│   └── detail/
│       └── detail.vue      # 详情页
├── components/             # 自定义组件目录
│   └── my-comp/
│       └── my-comp.vue     # 遵循 easycom 规范自动注册
├── static/                 # 静态资源（不会编译，直接拷贝）
│   ├── logo.png
│   └── mp-weixin/          # 微信小程序专用资源
├── store/                  # Vuex/Pinia 状态管理
├── api/                    # 接口封装
├── utils/                  # 工具函数
├── uni_modules/            # uni_modules 插件目录
├── platforms/              # 平台专用页面
├── nativeResources/        # 原生资源目录（App端）
│   ├── android/
│   └── ios/
├── pages.json              # 页面路由和全局配置（核心）
├── manifest.json           # 应用配置（AppID、权限等）
├── App.vue                 # 应用入口/全局生命周期
├── main.js                 # 入口文件/Vue 实例初始化
├── uni.scss                # 全局样式变量
└── package.json
```

### 3.2 核心配置文件详解

#### pages.json — 页面路由与全局配置

```json
{
  "globalStyle": {
    "navigationBarTextStyle": "black",
    "navigationBarTitleText": "我的应用",
    "navigationBarBackgroundColor": "#F8F8F8",
    "backgroundColor": "#F8F8F8"
  },
  "pages": [
    {
      "path": "pages/index/index",
      "style": {
        "navigationBarTitleText": "首页",
        "enablePullDownRefresh": true
      }
    },
    {
      "path": "pages/detail/detail",
      "style": {
        "navigationBarTitleText": "详情"
      }
    }
  ],
  "tabBar": {
    "color": "#7A7E83",
    "selectedColor": "#007AFF",
    "borderStyle": "black",
    "backgroundColor": "#ffffff",
    "list": [
      {
        "pagePath": "pages/index/index",
        "iconPath": "static/tab-home.png",
        "selectedIconPath": "static/tab-home-active.png",
        "text": "首页"
      },
      {
        "pagePath": "pages/mine/mine",
        "iconPath": "static/tab-mine.png",
        "selectedIconPath": "static/tab-mine-active.png",
        "text": "我的"
      }
    ]
  },
  "easycom": {
    "autoscan": true,
    "custom": {
      "^uni-(.*)": "@dcloudio/uni-ui/lib/uni-$1/uni-$1.vue"
    }
  },
  "subPackages": [
    {
      "root": "pages/sub",
      "pages": [
        { "path": "setting", "style": { "navigationBarTitleText": "设置" } }
      ]
    }
  ],
  "preloadRule": {
    "pages/index/index": {
      "network": "all",
      "packages": ["pages/sub"]
    }
  },
  "condition": {
    "current": 0,
    "list": [
      { "name": "详情页", "path": "pages/detail/detail", "query": "id=123" }
    ]
  }
}
```

**关键配置项说明：**

| 配置项 | 说明 |
|-------|------|
| `globalStyle` | 全局默认窗口样式（导航栏颜色、标题、背景色等） |
| `pages` | 页面路由数组，**第一项为入口页面** |
| `tabBar` | 底部导航栏配置，支持 2-5 个 tab |
| `easycom` | 组件自动导入规则 |
| `subPackages` | 分包配置，优化小程序启动速度 |
| `preloadRule` | 分包预加载规则 |
| `condition` | 开发调试模式配置 |

#### manifest.json — 应用配置

```json
{
  "name": "我的应用",
  "appid": "__UNI__XXXXXXX",
  "versionName": "1.0.0",
  "versionCode": "100",
  "mp-weixin": {
    "appid": "wx1234567890",
    "setting": { "urlCheck": false }
  },
  "app-plus": {
    "distribute": {
      "android": { "permissions": [] },
      "ios": {}
    }
  },
  "h5": {
    "devServer": { "port": 8080 },
    "router": { "mode": "history" },
    "title": "我的应用"
  }
}
```

#### App.vue — 应用入口

```vue
<script>
export default {
  onLaunch(options) {
    console.log('应用启动', options)
  },
  onShow(options) {
    console.log('应用进入前台')
  },
  onHide() {
    console.log('应用进入后台')
  }
}
</script>

<style>
/* 全局样式 */
page {
  background-color: #f5f5f5;
  font-size: 28rpx;
}
</style>
```

---

## 四、Vue3 语法在 uni-app 中的使用

### 4.1 页面基础结构

```vue
<template>
  <view class="container">
    <text>{{ message }}</text>
    <button @click="handleClick">点击</button>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'

const message = ref('Hello uni-app')
const count = ref(0)

const doubleCount = computed(() => count.value * 2)

onLoad((options) => {
  console.log('页面加载，参数：', options)
})

onShow(() => {
  console.log('页面显示')
})

onMounted(() => {
  console.log('组件挂载完成')
})

function handleClick() {
  count.value++
  message.value = `点击了 ${count.value} 次`
}
</script>

<style scoped>
.container {
  padding: 20rpx;
}
</style>
```

### 4.2 响应式数据

```js
import { ref, reactive, toRefs } from 'vue'

// ref — 基础类型
const name = ref('张三')
const age = ref(25)

// reactive — 对象类型
const userInfo = reactive({
  name: '张三',
  age: 25,
  address: { city: '北京' }
})

// 解构时保持响应式
const { name, age } = toRefs(userInfo)
```

### 4.3 数据绑定与指令

```vue
<template>
  <view>
    <!-- 文本插值 -->
    <text>{{ message }}</text>

    <!-- 属性绑定 -->
    <image :src="imgUrl" />

    <!-- 双向绑定 -->
    <input v-model="keyword" placeholder="搜索" />

    <!-- 条件渲染 -->
    <view v-if="isVip">VIP 内容</view>
    <view v-else>普通内容</view>
    <view v-show="isVisible">v-show 控制显示</view>

    <!-- 列表渲染 -->
    <view v-for="(item, index) in list" :key="item.id">
      {{ index }}. {{ item.name }}
    </view>

    <!-- 事件处理 -->
    <button @click="submit">提交</button>
    <button @click.stop="onTap">阻止冒泡</button>
  </view>
</template>
```

### 4.4 计算属性与侦听器

```js
import { ref, computed, watch, watchEffect } from 'vue'

const price = ref(100)
const quantity = ref(2)

// 计算属性 — 有缓存
const total = computed(() => price.value * quantity.value)

// 侦听单个
watch(price, (newVal, oldVal) => {
  console.log(`价格从 ${oldVal} 变为 ${newVal}`)
})

// 侦听多个
watch([price, quantity], ([newPrice, newQty]) => {
  console.log('价格或数量变化', newPrice, newQty)
})

// 深度侦听
const obj = ref({ a: { b: 1 } })
watch(obj, (val) => { /* ... */ }, { deep: true })

// 自动追踪依赖
watchEffect(() => {
  console.log('总价：', total.value)
})
```

### 4.5 组件通信

```vue
<!-- 父组件 -->
<template>
  <child-comp
    :title="pageTitle"
    @update="handleUpdate"
  />
</template>

<script setup>
import { ref } from 'vue'

const pageTitle = ref('标题')

function handleUpdate(data) {
  console.log('子组件传来：', data)
}
</script>
```

```vue
<!-- 子组件 child-comp.vue -->
<template>
  <view @click="emitData">
    <text>{{ title }}</text>
  </view>
</template>

<script setup>
const props = defineProps({
  title: { type: String, default: '' }
})

const emit = defineEmits(['update'])

function emitData() {
  emit('update', { value: '新数据' })
}
</script>
```

---

## 五、生命周期

### 5.1 应用生命周期（App.vue）

| 钩子 | 触发时机 |
|------|---------|
| `onLaunch` | 应用初始化完成时（全局只触发一次） |
| `onShow` | 应用从后台进入前台 |
| `onHide` | 应用从前台进入后台 |
| `onError` | 发生脚本错误或 API 调用失败 |

### 5.2 页面生命周期

```
onLoad → onShow → onReady → (用户交互) → onHide / onUnload
```

| 钩子 | 说明 | 常见用途 |
|------|------|---------|
| `onLoad(options)` | 页面加载，接收路由参数 | 获取页面参数、请求初始数据 |
| `onShow` | 页面显示（每次可见时触发） | 刷新数据、恢复状态 |
| `onReady` | 页面首次渲染完成 | DOM 操作、初始化图表 |
| `onHide` | 页面隐藏 | 暂停定时器 |
| `onUnload` | 页面卸载 | 清理资源、移除事件监听 |
| `onPullDownRefresh` | 下拉刷新 | 重新加载数据 |
| `onReachBottom` | 滚动到底部 | 加载更多（分页） |
| `onPageScroll(e)` | 页面滚动 | 吸顶效果、回到顶部按钮 |
| `onShareAppMessage` | 点击分享 | 自定义分享内容 |

**Vue3 Composition API 用法：**

```js
import { onLoad, onShow, onReady, onPullDownRefresh } from '@dcloudio/uni-app'

onLoad((options) => {
  const id = options.id // 获取路由参数
  fetchDetail(id)
})

onPullDownRefresh(() => {
  refreshData().finally(() => {
    uni.stopPullDownRefresh()
  })
})
```

---

## 六、路由与页面跳转

### 6.1 路由方式对比

| API | Navigator 组件 | 说明 |
|-----|---------------|------|
| `uni.navigateTo` | `<navigator open-type="navigate">` | 打开新页面（入栈） |
| `uni.redirectTo` | `<navigator open-type="redirect">` | 页面重定向（替换当前页） |
| `uni.reLaunch` | `<navigator open-type="reLaunch">` | 关闭所有页面，打开指定页面 |
| `uni.switchTab` | `<navigator open-type="switchTab">` | 切换 Tab 页面 |
| `uni.navigateBack` | `<navigator open-type="navigateBack">` | 返回上一页（出栈） |

### 6.2 页面跳转与传参

```js
// 跳转并传参
uni.navigateTo({
  url: '/pages/detail/detail?id=123&name=商品A'
})

// 目标页面接收参数
onLoad((options) => {
  console.log(options.id)   // "123"
  console.log(options.name) // "商品A"
})

// 传递复杂数据（需编码）
const data = encodeURIComponent(JSON.stringify({ list: [1, 2, 3] }))
uni.navigateTo({
  url: `/pages/detail/detail?data=${data}`
})

// 返回上一页并传递数据
uni.navigateBack({
  delta: 1
})
```

### 6.3 页面栈管理

```
navigateTo:   [A] → [A, B]      // B 入栈
redirectTo:   [A, B] → [A, C]   // B 出栈，C 入栈
navigateBack: [A, B] → [A]      // B 出栈
switchTab:    [A, B] → [Tab1]   // 清空栈
reLaunch:     [A, B] → [C]      // 清空栈
```

通过 `getCurrentPages()` 获取当前页面栈数组。

### 6.4 跨页面通信

```js
// 页面 A：触发事件
uni.$emit('updateData', { msg: '来自A的数据' })

// 页面 B：监听事件
onLoad(() => {
  uni.$on('updateData', (data) => {
    console.log(data.msg) // "来自A的数据"
  })
})

// 页面卸载时移除监听（防止内存泄漏）
onUnload(() => {
  uni.$off('updateData')
})
```

---

## 七、内置组件

### 7.1 组件分类总览

#### 视图容器

| 组件 | 说明 | 使用场景 |
|------|------|---------|
| `<view>` | 基础视图容器（类似 div） | 布局容器 |
| `<scroll-view>` | 可滚动视图 | 横向/纵向滚动列表 |
| `<swiper>` | 轮播图容器 | Banner、图片轮播 |
| `<movable-view>` | 可拖动视图 | 拖拽交互 |
| `<cover-view>` | 覆盖原生组件的文本视图 | 地图/视频上的文字 |

#### 基础内容

| 组件 | 说明 |
|------|------|
| `<text>` | 文本（支持嵌套、长按选择） |
| `<rich-text>` | 富文本展示 |
| `<icon>` | 图标 |
| `<progress>` | 进度条 |

#### 表单组件

| 组件 | 说明 |
|------|------|
| `<button>` | 按钮 |
| `<input>` | 输入框 |
| `<textarea>` | 多行文本输入 |
| `<checkbox>` | 复选框 |
| `<radio>` | 单选框 |
| `<picker>` | 选择器（时间/日期/地区） |
| `<slider>` | 滑动选择器 |
| `<switch>` | 开关 |
| `<form>` | 表单 |

#### 媒体组件

| 组件 | 说明 |
|------|------|
| `<image>` | 图片 |
| `<video>` | 视频 |
| `<camera>` | 相机 |
| `<audio>` | 音频 |
| `<live-player>` | 直播播放 |

#### 其他

| 组件 | 说明 |
|------|------|
| `<navigator>` | 页面链接跳转 |
| `<map>` | 地图 |
| `<canvas>` | 画布 |
| `<web-view>` | 嵌入网页 |
| `<ad>` | 广告 |

### 7.2 easycom 自动注册机制

组件放置在 `components/组件名/组件名.vue` 路径下，即可在任何页面直接使用，无需手动 import 和注册：

```
components/
  └── my-card/
      └── my-card.vue    ← 自动注册，直接使用 <my-card />
```

也可在 `pages.json` 中配置自定义规则：

```json
{
  "easycom": {
    "custom": {
      "^uni-(.*)": "@dcloudio/uni-ui/lib/uni-$1/uni-$1.vue"
    }
  }
}
```

---

## 八、常用 API

### 8.1 网络请求

```js
// 基础请求
uni.request({
  url: 'https://api.example.com/data',
  method: 'GET',
  data: { page: 1 },
  header: { 'Authorization': 'Bearer token' },
  success(res) {
    console.log(res.data)
  },
  fail(err) {
    console.error(err)
  }
})

// Promise 方式（Vue3）
try {
  const res = await uni.request({
    url: 'https://api.example.com/data',
    method: 'POST',
    data: { name: '张三' }
  })
  console.log(res.data)
} catch (err) {
  console.error(err)
}
```

**封装建议：**

```js
// utils/request.js
const BASE_URL = 'https://api.example.com'

export function request(options) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + options.url,
      method: options.method || 'GET',
      data: options.data,
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${uni.getStorageSync('token')}`,
        ...options.header
      },
      success(res) {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else if (res.statusCode === 401) {
          uni.navigateTo({ url: '/pages/login/login' })
          reject(res)
        } else {
          uni.showToast({ title: '请求失败', icon: 'none' })
          reject(res)
        }
      },
      fail: reject
    })
  })
}
```

### 8.2 数据缓存

```js
// 同步存储
uni.setStorageSync('userInfo', { name: '张三', age: 25 })
const user = uni.getStorageSync('userInfo')
uni.removeStorageSync('userInfo')
uni.clearStorageSync()

// 异步存储
uni.setStorage({
  key: 'token',
  data: 'abc123',
  success() { console.log('存储成功') }
})
```

### 8.3 交互反馈

```js
// 提示框
uni.showToast({ title: '操作成功', icon: 'success', duration: 1500 })
uni.showToast({ title: '加载中...', icon: 'loading' })

// 模态对话框
uni.showModal({
  title: '提示',
  content: '确定删除此项？',
  success(res) {
    if (res.confirm) { /* 删除 */ }
  }
})

// 操作菜单
uni.showActionSheet({
  itemList: ['拍照', '从相册选择'],
  success(res) {
    console.log('选择了第', res.tapIndex, '项')
  }
})

// 加载提示
uni.showLoading({ title: '加载中' })
// ... 请求完成后
uni.hideLoading()
```

### 8.4 媒体 API

```js
// 选择图片
uni.chooseImage({
  count: 9,
  sizeType: ['compressed'],
  sourceType: ['album', 'camera'],
  success(res) {
    const tempFiles = res.tempFilePaths
  }
})

// 图片预览
uni.previewImage({
  urls: ['https://example.com/1.jpg', 'https://example.com/2.jpg'],
  current: 0
})

// 上传文件
uni.uploadFile({
  url: 'https://api.example.com/upload',
  filePath: tempFilePath,
  name: 'file',
  formData: { type: 'avatar' },
  success(res) {
    console.log(JSON.parse(res.data))
  }
})
```

### 8.5 设备与系统

```js
// 获取系统信息
const sysInfo = uni.getSystemInfoSync()
console.log(sysInfo.platform)      // "ios" | "android" | "devtools"
console.log(sysInfo.windowWidth)   // 窗口宽度
console.log(sysInfo.statusBarHeight) // 状态栏高度

// 获取网络状态
uni.getNetworkType({
  success(res) {
    console.log(res.networkType) // "wifi" | "4g" | "none"
  }
})

// 扫码
uni.scanCode({
  success(res) {
    console.log('扫码结果：', res.result)
  }
})

// 剪贴板
uni.setClipboardData({ data: '复制内容' })
```

### 8.6 位置与地图

```js
// 获取位置
uni.getLocation({
  type: 'gcj02',
  success(res) {
    console.log(res.latitude, res.longitude)
  }
})

// 打开地图选择位置
uni.chooseLocation({
  success(res) {
    console.log(res.name, res.address, res.latitude)
  }
})
```

---

## 九、条件编译

### 9.1 基本语法

条件编译使用特殊注释标记，在编译时按平台生成对应代码：

```
#ifdef PLATFORM    → 仅在指定平台编译
#ifndef PLATFORM   → 除指定平台外都编译
#endif             → 结束条件编译块
```

### 9.2 平台标识符

| 标识符 | 平台 |
|-------|------|
| `APP` / `APP-PLUS` | App（iOS + Android） |
| `APP-ANDROID` | 仅 Android App |
| `APP-IOS` | 仅 iOS App |
| `H5` / `WEB` | Web 端 |
| `MP-WEIXIN` | 微信小程序 |
| `MP-ALIPAY` | 支付宝小程序 |
| `MP-TOUTIAO` | 抖音小程序 |
| `MP-BAIDU` | 百度小程序 |
| `MP` | 所有小程序 |
| `VUE3` | 使用 Vue3 时 |

### 9.3 使用示例

**模板中：**
```html
<template>
  <view>
    <!-- #ifdef MP-WEIXIN -->
    <button open-type="share">微信分享</button>
    <!-- #endif -->

    <!-- #ifdef H5 -->
    <button @click="webShare">网页分享</button>
    <!-- #endif -->

    <!-- #ifndef MP -->
    <view>非小程序平台显示</view>
    <!-- #endif -->
  </view>
</template>
```

**JavaScript 中：**
```js
// #ifdef APP-PLUS
import { NativeModule } from './native'
NativeModule.init()
// #endif

// #ifdef H5
document.title = '页面标题'
// #endif

// #ifdef MP-WEIXIN
wx.login({ success(res) { /* ... */ } })
// #endif
```

**CSS 中：**
```css
/* #ifdef H5 */
.container { max-width: 750px; margin: 0 auto; }
/* #endif */

/* #ifndef APP-PLUS */
.native-only { display: none; }
/* #endif */
```

**pages.json 中：**
```json
{
  "pages": [
    {
      "path": "pages/index/index",
      "style": {
        "navigationBarTitleText": "首页",
        "mp-weixin": {
          "navigationBarTextStyle": "white"
        },
        "h5": {
          "titleNView": false
        }
      }
    }
  ]
}
```

**静态资源条件编译：**

```
static/
  ├── logo.png              # 公共资源
  ├── mp-weixin/
  │   └── wx-share.png      # 仅微信小程序打包
  └── h5/
      └── web-icon.png      # 仅 H5 打包
```

---

## 十、样式与布局

### 10.1 尺寸单位

| 单位 | 说明 |
|------|------|
| `rpx` | 响应式像素，750rpx = 屏幕宽度（推荐） |
| `px` | 固定像素 |
| `%` | 百分比 |
| `vh/vw` | 视口单位（仅 H5） |
| `rem` | 相对根元素字体大小（仅 H5） |

**rpx 换算规则：** 设计稿宽度 750px 时，1px = 1rpx。设计稿宽度 375px 时，1px = 2rpx。

### 10.2 Flex 布局

```css
/* 水平居中排列 */
.row {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

/* 垂直居中 */
.center {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

/* 自适应布局 */
.flex-item {
  flex: 1;
}
```

### 10.3 全局样式变量 (uni.scss)

```scss
// uni.scss — 全局可用，无需 @import
$brand-color: #007AFF;
$text-color: #333333;
$text-color-light: #999999;
$bg-color: #F5F5F5;
$border-color: #E5E5E5;
$spacing: 20rpx;
$radius: 12rpx;
```

### 10.4 常用样式技巧

```css
/* 安全区域适配（iPhone 底部） */
.bottom-bar {
  padding-bottom: constant(safe-area-inset-bottom); /* iOS < 11.2 */
  padding-bottom: env(safe-area-inset-bottom);      /* iOS >= 11.2 */
}

/* 文本省略 */
.ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 多行省略 */
.ellipsis-2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

/* 1px 边框（高清屏） */
.border-bottom {
  position: relative;
}
.border-bottom::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 1px;
  background: #eee;
  transform: scaleY(0.5);
}
```

---

## 十一、状态管理

### 11.1 Pinia（Vue3 推荐）

```bash
npm install pinia
```

```js
// main.js
import { createSSRApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

export function createApp() {
  const app = createSSRApp(App)
  const pinia = createPinia()
  app.use(pinia)
  return { app }
}
```

```js
// store/user.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref(uni.getStorageSync('token') || '')
  const userInfo = ref(null)

  const isLoggedIn = computed(() => !!token.value)

  function setToken(val) {
    token.value = val
    uni.setStorageSync('token', val)
  }

  function setUserInfo(info) {
    userInfo.value = info
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    uni.removeStorageSync('token')
  }

  return { token, userInfo, isLoggedIn, setToken, setUserInfo, logout }
})
```

```vue
<!-- 页面中使用 -->
<script setup>
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

if (!userStore.isLoggedIn) {
  uni.navigateTo({ url: '/pages/login/login' })
}
</script>
```

### 11.2 全局数据共享（简易方案）

```js
// main.js
import { createSSRApp } from 'vue'
import App from './App.vue'

export function createApp() {
  const app = createSSRApp(App)
  app.config.globalProperties.$globalData = {
    baseUrl: 'https://api.example.com'
  }
  return { app }
}
```

---

## 十二、性能优化

### 12.1 架构原理

非 H5 端采用**逻辑层与渲染层分离**架构。逻辑层在独立的 jscore 引擎中运行 JS，渲染层负责界面绘制。两层通过消息通信，Android 上单次通信耗时可达数十毫秒。

### 12.2 核心优化策略

#### 数据优化

```js
// ❌ 非视图数据不要放在 data 中
const data = reactive({
  list: [],       // 视图用 ✅
  tempCache: {}   // 非视图用 ❌ — 会触发不必要的渲染
})

// ✅ 非视图数据使用普通变量
let tempCache = {}
const list = ref([])
```

#### 长列表优化

```vue
<!-- 使用 uni-list 组件（自动选择最优渲染策略） -->
<uni-list>
  <uni-list-item v-for="item in list" :key="item.id" :title="item.name" />
</uni-list>

<!-- 虚拟列表方案 -->
<!-- 仅渲染可视区域内的元素，大幅减少 DOM 节点 -->
```

#### 图片优化

```vue
<!-- ✅ 指定尺寸，使用 lazy-load -->
<image
  :src="item.thumb"
  mode="aspectFill"
  style="width: 200rpx; height: 200rpx;"
  lazy-load
/>

<!-- ❌ 避免在单页面加载大量高分辨率图片 -->
```

#### 减少通信开销

```js
// ❌ 频繁监听滚动
onPageScroll((e) => {
  // 每次滚动都触发通信
})

// ✅ 使用 CSS 动画代替 JS 定时器
// ✅ 使用 renderjs（App端）或 wxs（小程序端）在渲染层直接操作
```

#### 页面初始化优化

```js
// 分批渲染，延迟加载重元素
const showHeavyContent = ref(false)

onReady(() => {
  setTimeout(() => {
    showHeavyContent.value = true
  }, 200)
})
```

#### 启动速度优化

- 使用分包加载，减少主包体积（小程序主包限制 2MB）
- manifest.json 开启 tree-shaking
- 减少启动时的同步操作
- 精简 `onLaunch` 中的逻辑

#### 包体积优化

- 开启 tree-shaking，H5 gzip 后约 162KB
- 图片资源使用 CDN，不放入 static
- 合理使用分包和分包预加载
- 移除未使用的组件和插件

---

## 十三、原生能力集成

### 13.1 Android 原生资源配置

```
nativeResources/
  └── android/
      ├── AndroidManifest.xml   # 权限和组件声明
      ├── assets/               # 原生资源
      └── res/                  # 原生资源文件
```

```xml
<!-- AndroidManifest.xml -->
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    package="com.example.myapp">

    <!-- 权限声明 -->
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />

    <application>
        <!-- 自定义 URL Scheme -->
        <activity android:name="io.dcloud.PandoraEntryActivity">
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="myapp" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

### 13.2 uni 原生插件

```js
// 引用原生插件
const plugin = uni.requireNativePlugin('pluginName')

// 调用插件方法
plugin.doSomething({
  param: 'value'
}, (result) => {
  console.log(result)
})
```

---

## 十四、uniCloud 云开发

### 14.1 概述

uniCloud 是 DCloud 联合多家云服务商推出的基于 serverless 的云开发平台，支持：

- **云函数/云对象** — 服务端逻辑
- **云数据库** — JSON 文档数据库
- **云存储** — 文件上传下载
- **前端网页托管** — 静态资源托管

### 14.2 配套服务

| 服务 | 说明 |
|------|------|
| uni-id | 统一用户体系 |
| uni-pay | 统一支付 |
| uni-push | 消息推送 |
| uni-admin | 管理后台 |
| uni-search | 全文搜索 |
| uni-cms | 内容管理 |

---

## 十五、实战模式与最佳实践

### 15.1 项目初始化模板

```bash
# 创建项目
npx degit dcloudio/uni-preset-vue#vite-ts my-project
cd my-project
npm install

# 安装常用依赖
npm install pinia
npm install @dcloudio/uni-ui
```

推荐目录结构：

```
src/
  ├── api/            # 接口定义
  │   ├── index.js    # 请求封装
  │   ├── user.js     # 用户相关接口
  │   └── order.js    # 订单相关接口
  ├── components/     # 公共组件
  ├── composables/    # 组合式函数
  │   ├── useAuth.js
  │   └── useRequest.js
  ├── pages/          # 页面
  ├── store/          # 状态管理
  ├── static/         # 静态资源
  ├── styles/         # 公共样式
  │   └── mixins.scss
  ├── utils/          # 工具函数
  │   ├── format.js
  │   └── validate.js
  ├── App.vue
  ├── main.js
  ├── manifest.json
  ├── pages.json
  └── uni.scss
```

### 15.2 请求拦截器模式

```js
// api/index.js
const BASE_URL = import.meta.env.VITE_API_URL || 'https://api.example.com'

let isRefreshing = false
let requestQueue = []

export function request(options) {
  return new Promise((resolve, reject) => {
    uni.showLoading({ title: '加载中', mask: true })

    uni.request({
      url: BASE_URL + options.url,
      method: options.method || 'GET',
      data: options.data,
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${uni.getStorageSync('token')}`,
        ...options.header
      },
      success(res) {
        const { statusCode, data } = res
        if (statusCode === 200 && data.code === 0) {
          resolve(data.data)
        } else if (statusCode === 401) {
          // Token 过期处理
          uni.removeStorageSync('token')
          uni.reLaunch({ url: '/pages/login/login' })
          reject(new Error('未登录'))
        } else {
          uni.showToast({ title: data.msg || '请求失败', icon: 'none' })
          reject(data)
        }
      },
      fail(err) {
        uni.showToast({ title: '网络异常', icon: 'none' })
        reject(err)
      },
      complete() {
        uni.hideLoading()
      }
    })
  })
}

// 便捷方法
export const get = (url, data) => request({ url, method: 'GET', data })
export const post = (url, data) => request({ url, method: 'POST', data })
```

### 15.3 登录鉴权模式

```js
// composables/useAuth.js
import { useUserStore } from '@/store/user'

export function useAuth() {
  const userStore = useUserStore()

  // 检查登录状态
  function checkLogin() {
    if (!userStore.isLoggedIn) {
      uni.navigateTo({ url: '/pages/login/login' })
      return false
    }
    return true
  }

  // 微信登录
  async function wxLogin() {
    // #ifdef MP-WEIXIN
    const { code } = await uni.login({ provider: 'weixin' })
    const res = await post('/auth/wx-login', { code })
    userStore.setToken(res.token)
    userStore.setUserInfo(res.userInfo)
    // #endif
  }

  return { checkLogin, wxLogin }
}
```

### 15.4 分页加载模式

```vue
<template>
  <view>
    <view v-for="item in list" :key="item.id" class="item">
      <text>{{ item.title }}</text>
    </view>
    <view v-if="loading" class="loading">加载中...</view>
    <view v-if="finished" class="finished">没有更多了</view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { onLoad, onReachBottom, onPullDownRefresh } from '@dcloudio/uni-app'
import { get } from '@/api'

const list = ref([])
const page = ref(1)
const pageSize = 20
const loading = ref(false)
const finished = ref(false)

async function loadData(isRefresh = false) {
  if (loading.value) return
  if (finished.value && !isRefresh) return

  if (isRefresh) {
    page.value = 1
    finished.value = false
  }

  loading.value = true
  try {
    const res = await get('/list', { page: page.value, pageSize })
    if (isRefresh) {
      list.value = res.list
    } else {
      list.value.push(...res.list)
    }
    if (res.list.length < pageSize) {
      finished.value = true
    }
    page.value++
  } finally {
    loading.value = false
  }
}

onLoad(() => loadData())

onReachBottom(() => loadData())

onPullDownRefresh(async () => {
  await loadData(true)
  uni.stopPullDownRefresh()
})
</script>
```

### 15.5 全局错误处理

```js
// App.vue
export default {
  onError(err) {
    console.error('全局错误：', err)
    // 上报错误日志
  },
  onLaunch() {
    // 监听网络变化
    uni.onNetworkStatusChange((res) => {
      if (!res.isConnected) {
        uni.showToast({ title: '网络已断开', icon: 'none' })
      }
    })
  }
}
```

---

## 十六、跨平台适配要点

### 16.1 各平台差异速查

| 特性 | H5 | 微信小程序 | App |
|------|-----|----------|-----|
| DOM 操作 | 支持 | 不支持 | 不支持 |
| Cookie | 支持 | 不支持 | 不支持 |
| 浏览器对象 (window/document) | 支持 | 不支持 | 不支持 |
| NPM 包 | 完整支持 | 部分支持 | 部分支持 |
| 自定义组件 | 完整 Vue | 有限制 | 有限制 |
| 包大小限制 | 无 | 主包 2MB | 无 |
| 分包 | 不需要 | 需要 | 不需要 |
| 原生能力 | 有限 | 微信 API | 完整 |

### 16.2 适配建议

1. **避免使用浏览器特有 API**（document、window），用 uni API 替代
2. **样式使用 rpx**，不使用 rem/vw
3. **标签使用 `<view>` 替代 `<div>`**，`<text>` 替代 `<span>`
4. **资源路径使用绝对路径或 `@/` 别名**
5. **利用条件编译处理平台差异**
6. **小程序端注意包体积**，合理使用分包

---

## 十七、调试与发布

### 17.1 调试方式

| 平台 | 调试方式 |
|------|---------|
| H5 | 浏览器 DevTools |
| 微信小程序 | 微信开发者工具 |
| 支付宝小程序 | 支付宝 IDE |
| App | HBuilderX 真机调试 / Android Studio / Xcode |

### 17.2 发布流程

```bash
# 1. 构建生产版本
npm run build:mp-weixin     # 微信小程序
npm run build:h5             # Web
npm run build:app            # App

# 2. 各平台发布
# 微信小程序 → 微信开发者工具上传
# H5 → 部署到 Web 服务器
# App → HBuilderX 云打包 / 本地打包
```

### 17.3 多环境配置

```js
// .env.development
VITE_API_URL=https://dev-api.example.com
VITE_ENV=development

// .env.production
VITE_API_URL=https://api.example.com
VITE_ENV=production
```

```js
// 使用
const apiUrl = import.meta.env.VITE_API_URL
```

---

## 十八、常见问题与解决方案

### Q1: 页面间传递复杂数据

```js
// 方案一：事件总线
uni.$emit('setData', complexObj)

// 方案二：全局存储
uni.setStorageSync('tempData', JSON.stringify(data))

// 方案三：Pinia
const store = useSharedStore()
store.setTempData(data)
```

### Q2: 小程序包体积超限

- 启用分包：`subPackages` 配置
- 图片使用 CDN 地址
- 移除未使用的组件和页面
- 压缩静态资源

### Q3: 样式在不同平台不一致

- 使用 rpx 统一尺寸
- 避免使用平台特有 CSS 特性
- 使用条件编译处理差异样式
- 测试时覆盖主流设备

### Q4: v-for 和 v-if 不能同时使用

```vue
<!-- ❌ 错误 -->
<view v-for="item in list" v-if="item.visible" :key="item.id" />

<!-- ✅ 正确：使用 computed 过滤 -->
<view v-for="item in visibleList" :key="item.id" />
```

```js
const visibleList = computed(() => list.value.filter(item => item.visible))
```

### Q5: 小程序端组件样式穿透

```css
/* Vue3 中使用 :deep() */
:deep(.child-class) {
  color: red;
}
```

---

## 十九、推荐资源

| 资源 | 地址 |
|------|------|
| 官方文档 | https://uniapp.dcloud.net.cn/ |
| 插件市场 | https://ext.dcloud.net.cn/ |
| uni-ui 组件库 | https://uniapp.dcloud.net.cn/component/uniui/uni-ui.html |
| uniCloud 文档 | https://doc.dcloud.net.cn/uniCloud/ |
| HBuilderX 下载 | https://www.dcloud.io/hbuilderx.html |
| 社区论坛 | https://ask.dcloud.net.cn/ |

---

> 本文档基于 uni-app 官方文档整理，建议结合官方文档获取最新 API 细节和平台更新信息。
