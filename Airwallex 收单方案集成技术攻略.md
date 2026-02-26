# Airwallex 收单方案集成技术攻略

> 基于 Airwallex 官方收单集成文档整理，涵盖一次性支付、循环扣款（MIT/CIT）、Google Pay / Apple Pay、退款、Webhook 等全流程。

---

## 目录

1. [产品概览](#1-产品概览)
2. [接入方式对比与选型](#2-接入方式对比与选型)
3. [对接准备](#3-对接准备)
4. [一次性支付集成](#4-一次性支付集成)
   - 4.1 托管页面模式 (HPP)
   - 4.2 模块嵌入模式 (Drop-in)
   - 4.3 字段嵌入模式 (Embedded Elements)
5. [循环扣款集成](#5-循环扣款集成)
   - 5.1 MIT 与 CIT 概念
   - 5.2 托管页面模式循环扣款
   - 5.3 模块嵌入模式循环扣款
   - 5.4 字段嵌入模式循环扣款
6. [Google Pay 与 Apple Pay 接入](#6-google-pay-与-apple-pay-接入)
7. [退款处理](#7-退款处理)
8. [Webhook 订阅与配置](#8-webhook-订阅与配置)
9. [风控字段传入](#9-风控字段传入)
10. [自动货币兑换](#10-自动货币兑换)
11. [测试与上线](#11-测试与上线)
12. [附录](#12-附录)

---

## 1. 产品概览

Airwallex 收单产品支持以多种方式接受在线支付：

| 支付类型 | 说明 |
|---------|------|
| **卡收单** | 作为 Visa 和 Mastercard 卡组织会员，接收主流银行卡支付 |
| **本地钱包收单** | 微信钱包、支付宝等本地支付方式 |

**支持的支付形态：**
- 一次性支付
- 循环扣款（订阅 / 一键支付）

**本地钱包支持列表：** https://www.airwallex.com/docs/payments__payment-methods-overview

---

## 2. 接入方式对比与选型

|  | 托管页面 (HPP) | 模块嵌入 (Drop-in) | 字段嵌入 (Embedded Elements) |
|--|---------------|-------------------|---------------------------|
| **对接难度** | 低 | 中 | 高 |
| **适用场景** | 快速上线，开发资源有限，无自研收银台 | 需嵌入自有页面，适度定制化 UI | 需高度定制支付体验，自有收银台 |
| **自定义程度** | 低 | 中 | 高 |
| **跳转方式** | 跳转到 Airwallex 支付页面 | 本地嵌入模块，无需跳转 | 本地嵌入模块，无需跳转 |
| **说明** | 前端跳转至 Airwallex 支付页面，用户直接在该页面完成支付 | Airwallex 提供即插即用支付组件，嵌入客户网站 | 仅将关键支付字段（卡号、有效期、CVV）以 iframe 嵌入自定义表单 |

> **选型建议：** 托管页面和模块嵌入模式会自动展示所有支持的支付方式。字段嵌入方式接入 APM 时需要额外对接。

### 支付页面最佳实践

- 订单概要：展示订单商品、运费、金额和币种
- 支付组件：前端校验卡号、有效期和 CVC
- 包含持卡人姓名
- 包含账单地址收集

---

## 3. 对接准备

### 3.1 API 相关文档

| 文档内容 | 地址 |
|---------|------|
| API 文档 | https://www.airwallex.com/docs/api#/Introduction |
| 支付组件 GitHub（CDN 集成） | https://github.com/airwallex/airwallex-payment-demo/tree/master/integrations/cdn |
| 支付组件 SDK 加载文档 | https://github.com/airwallex/airwallex-payment-demo/tree/master/docs#loadairwallex |
| 前端代码示例 | https://www.airwallex.com/docs/js/ |
| 支付方式列表和详情 | https://www.airwallex.com/docs/payments__payment-methods-overview |
| 收单官方文档 | https://www.airwallex.com/docs/online-payments__starting-with-payments |
| 测试卡 | https://www.airwallex.com/docs/payments__test-card-numbers |
| Webhook 订阅 | https://www.airwallex.com/docs/developer-tools__listen-for-webhook-events |
| Postman 脚本 | https://www.airwallex.com/docs/developer-tools__quickstart |
| 测试店铺 | https://demo-pacheckoutdemo.airwallex.com/shopping-cart |

### 3.2 获取 API Key

1. 登录空中云汇账号后台 → 开发者 → API Keys
2. 点击**创建受限的 API Key**，勾选收单 API 功能的「编辑」和「查看」权限
3. 输入登录密码完成创建
4. 复制 Client ID 和 API Key（退出后无法再复制，需重新生成）

### 3.3 导入 Postman 脚本

1. 访问 https://www.airwallex.com/docs/developer-tools__quickstart
2. 点击 **Run in Postman** 按钮，按文档提示开始测试
3. 也可使用 APIpost，导入 JSON 文件（请联系客户经理获取）
4. 通过 **Obtain access token** 接口获取 token，收单接口在 Online Payments 文件夹下

### 3.4 环境说明

| 环境 | API Base URL | 前端 env 参数 |
|-----|-------------|--------------|
| 测试环境 | `https://api-demo.airwallex.com` | `demo` |
| 生产环境 | `https://api.airwallex.com` | `prod` |

---

## 4. 一次性支付集成

三种模式的后端 API 调用完全相同，区别仅在前端集成方式。

### 4.0 通用后端：获取 Access Token

```
POST https://api-demo.airwallex.com/api/v1/authentication/login
```

- 通过 Client ID 和 API Key 获取访问令牌
- 有效期：**30 分钟**
- 建议缓存在本地，**20 分钟后重新获取**

### 4.1 托管页面模式 (HPP)

**核心步骤：**
1. 调用 Obtain access token API 获取 Token
2. 后端发起 Create Payment Intent API，创建支付订单
3. 前端使用 Airwallex SDK 渲染支付按钮并跳转
4. 支付完成后，获得支付结果

#### 后端：Create a Payment Intent

```
POST https://api-demo.airwallex.com/api/v1/pa/payment_intents/create
```

**Request 示例：**

```json
{
  "request_id": "{{$guid}}",
  "merchant_order_id": "O29511517052021S156927",
  "amount": "100",
  "currency": "USD",
  "customer": {
    "email": "john.doe@airwallex.com",
    "first_name": "John",
    "last_name": "Doe",
    "merchant_customer_id": "Xx1234",
    "phone_number": "13800000000"
  },
  "order": {
    "products": [{
      "code": "8277-44692",
      "name": "Iphone 14",
      "desc": "phone",
      "quantity": 1,
      "sku": "b4121fb64929d818",
      "type": "physical",
      "unit_price": "100.00"
    }],
    "shipping": {
      "address": {
        "country_code": "CN",
        "state": "Shaanxi",
        "city": "Xi'an",
        "street": "Cai fu zhong xin",
        "postcode": "710103"
      },
      "first_name": "John",
      "last_name": "Doe",
      "phone_number": "15094044362",
      "shipping_method": "ManualDelivery"
    },
    "type": "physical_goods"
  },
  "return_url": "https://www.example.com/"
}
```

**关键字段说明：**
- `request_id` — 由商户创建，**不能重复**
- `return_url` — APM 回跳地址
- 订单信息会展示在支付页面

**Response 关键字段：**
- `id` — Payment Intent ID（传入前端组件）
- `client_secret` — 传入前端组件
- `status` — 初始为 `REQUIRES_PAYMENT_METHOD`
- `available_payment_method_types` — 可用的支付方式列表

#### 前端：HPP SDK 集成

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://static.airwallex.com/components/sdk/v1/index.js"></script>
</head>
<body>
  <button id="hpp">Pay Now</button>
  <script>
    (async () => {
      const { payments } = await window.AirwallexComponentsSDK.init({
        env: 'demo',
        enabledElements: ['payments'],
      });

      document.getElementById('hpp').addEventListener('click', () => {
        payments.redirectToCheckout({
          env: 'demo',
          mode: 'payment',
          intent_id: 'replace-with-your-intent-id',
          client_secret: 'replace-with-your-client-secret',
          currency: 'replace-with-your-currency',
          withBilling: true,
          requiredBillingContactFields: ['name', 'email', 'address']
        });
      });
    })();
  </script>
</body>
</html>
```

**可选参数：**

```javascript
payments.redirectToCheckout({
  // ...必填参数
  successUrl: 'https://www.example.com/success',  // 支付成功后跳转，必须 HTTPS
  logoUrl: 'https://www.example.com/logo.png',     // 商户 logo，必须 HTTPS
  locale: 'en',       // 前端语言：en, zh, ja, ko, ar, es, de, fr, it, nl
  methods: ['card', 'googlepay', 'applepay']  // 控制展示和排序支付方式
});
```

> **语言设置：** 默认根据浏览器语言显示，不支持的语言默认英文。参考文档：https://www.airwallex.com/docs/js/

**参考文档链接：**
- GitHub 示例：https://github.com/airwallex/airwallex-payment-demo/blob/master/integrations/cdn/hpp.html
- CDN 集成示例：https://github.com/airwallex/airwallex-payment-demo/tree/master/integrations/cdn
- 官方文档：https://www.airwallex.com/docs/js/payments/hosted-payment-page/

---

### 4.2 模块嵌入模式 (Drop-in)

**官方文档：** https://www.airwallex.com/docs/payments__drop-in-element

后端接口与 HPP 模式完全相同，区别在前端集成。

#### 前端：Drop-in SDK 集成

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://static.airwallex.com/components/sdk/v1/index.js"></script>
</head>
<body>
  <p id="loading">Loading...</p>
  <div id="dropIn"></div>
  <p id="error"></p>
  <p id="success" style="display:none">Payment Successful!</p>

  <script>
    (async () => {
      // 初始化 SDK
      await window.AirwallexComponentsSDK.init({
        env: 'demo',
        enabledElements: ['payments'],
      });

      // 创建 dropIn 元素
      const dropIn = await window.AirwallexComponentsSDK.createElement('dropIn', {
        intent_id: 'replace-with-your-intent-id',
        client_secret: 'replace-with-your-client-secret',
        currency: 'replace-with-your-currency',
        withBilling: true,
        requiredBillingContactFields: ['name', 'email', 'address']
      });

      // 挂载到 DOM
      dropIn.mount('dropIn');
    })();
  </script>

  <script>
    // 监听事件
    window.addEventListener('onReady', (event) => {
      document.getElementById('dropIn').style.display = 'block';
      document.getElementById('loading').style.display = 'none';
    });

    window.addEventListener('onSuccess', (event) => {
      document.getElementById('success').style.display = 'block';
    });

    window.addEventListener('onError', (event) => {
      const { error } = event.detail;
      document.getElementById('error').style.display = 'block';
      document.getElementById('error').innerHTML = error.message;
    });
  </script>
</body>
</html>
```

**可选参数：**

```javascript
const dropIn = await window.AirwallexComponentsSDK.createElement('dropIn', {
  // ...必填参数
  methods: ['card', 'googlepay', 'applepay']  // 控制展示和排序支付方式
});
```

**参考文档链接：**
- GitHub 示例：https://github.com/airwallex/airwallex-payment-demo/blob/master/integrations/cdn/dropin.html
- CDN 集成示例：https://github.com/airwallex/airwallex-payment-demo/tree/master/integrations/cdn
- 官方文档：https://www.airwallex.com/docs/js/payments/dropin/
- 游客结账：https://www.airwallex.com/docs/payments__drop-in-element__guest-user-checkout

---

### 4.3 字段嵌入模式 (Embedded Elements)

后端接口与前两种模式相同。前端支持两种卡片输入方式：

#### 分体式卡片输入

```javascript
// 创建分体式支付组件
const cardNumber = await window.AirwallexComponentsSDK.createElement('cardNumber');
const expiry = await window.AirwallexComponentsSDK.createElement('expiry');
const cvc = await window.AirwallexComponentsSDK.createElement('cvc');

// 挂载组件（id 必须与 DOM 容器一致）
cardNumber.mount('cardNumber');
expiry.mount('expiry');
cvc.mount('cvc');
```

#### 一体式卡片输入

```javascript
const card = await window.AirwallexComponentsSDK.createElement('card');
card.mount('card');
```

#### 提交支付

```javascript
document.getElementById('submit').addEventListener('click', () => {
  cardNumber.confirm({
    id: 'replace-with-your-intent-id',
    client_secret: 'replace-with-your-client-secret'
  })
  .then((response) => {
    // 支付成功处理
  })
  .catch((response) => {
    // 支付失败处理
    console.error('There was an error', response);
  });
});
```

**文档链接：**
- https://www.airwallex.com/docs/js/payments/card/
- https://www.airwallex.com/docs/js/payments/card-number/

---

## 5. 循环扣款集成

### 5.1 MIT 与 CIT 概念

| 类型 | 全称 | 说明 | 典型场景 |
|-----|------|------|---------|
| **CIT** | Customer Initiated Transaction | 交易由客户主动操作并授权发起 | 一键支付：用户使用已绑定的卡支付 |
| **MIT** | Merchant Initiated Transaction | 交易由商户基于客户之前授权发起 | 订阅、自动续费、分期付款 |

**应用场景举例：**
- **订阅（MIT 定期）：** 按月/按季收费的流媒体、APP 会员
- **自动扣款（MIT 不定期）：** 网约车平台服务完成后自动扣款
- **一键支付（CIT）：** 电商平台使用已绑定的卡直接支付

> **核心原理：** Airwallex 提供类似网关 Token（令牌服务）的能力，将 Customer 信息和经用户同意后的 Payment Method 存入 Payment Consent，得到一个 `consent_id` 用于后续支付。因此 **Customer** 和 **Payment Method** 是使用循环扣款的前提。

### 5.2 MIT 模式注意事项

MIT 的后续交易不需要消费者参与，支付失败时需注意：
1. 可进行**合理的扣费重试**，重试次数根据业务需要来定
2. 过于高频的重试会带来不必要的支付费用，**设定重试次数上限**
3. 超过限制后建立通知/联系客户的机制，引导客户更换卡片

### 5.3 订阅管理最佳实践

**订阅前：**
- 清晰标注折扣期的广告信息
- 要求持卡人**明确同意**订阅和定期扣款
- 发送电子版订阅服务条款（包含：确认同意、商品详情、金额/频率、取消链接）

**订阅后：**
- 试用期到期、协议变更时，至少**提前 7 天**发送通知并提供取消链接
- 交易收据披露试用期长度、金额和日期
- 提供**简便的在线取消/修改**方式
- 建立合理的投诉处理机制

### 5.4 循环扣款通用流程

#### Step 1: 创建 Customer

```
POST https://api-demo.airwallex.com/api/v1/pa/customers/create
```

```json
{
  "request_id": "0637816d-3c79-40f1-aee7-397a8821a521",
  "merchant_customer_id": "105d1929-ca0d-4bf6-8f77-cf5b8acdc41a",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@airwallex.com",
  "phone_number": "13800000000"
}
```

Response 返回 `customer_id`（如 `cus_bLYpNNnC60FhaHe8tdmqi1D5NKx`）和 `client_secret`，后续接口传参使用。

#### Step 1.5（仅绑卡模式）: 获取 Customer Client Secret

如果是**仅绑卡**场景（不创建 Payment Intent），需调用此接口获取 customer 的 `client_secret`：

```
GET https://api-demo.airwallex.com/api/v1/pa/customers/{customer_id}/generate_client_secret
```

**Response 示例：**

```json
{
  "client_secret": "eyJhbGciOiJIUzI1NiJ9...",
  "expired_time": "2021-04-09T04:18:43+0000"
}
```

> 此 `client_secret` 用于前端仅绑卡流程，替代 intent 的 `client_secret`。

#### Step 2: 创建 Payment Intent（带 customer_id）

```
POST https://api-demo.airwallex.com/api/v1/pa/payment_intents/create
```

在请求体中额外传入 `customer_id`：

```json
{
  "request_id": "b3ed5c1b-07af-4175-a6f6-f1481c30cdd6",
  "amount": 5000,
  "currency": "EUR",
  "merchant_order_id": "9c6476f7-951a-40c7-bcd4-aae91c121803",
  "customer_id": "cus_bLYpNNnC60FhaHe8tdmqi1D5NKx",
  "order": { ... }
}
```

### 5.5 CIT 模式对接

**首次绑卡并支付（HPP/Drop-in）：**
1. 后端创建 Customer → 获取 `customer_id`
2. 后端创建 Payment Intent → 传入 `customer_id`
3. 前端传入 `intent_id`、`client_secret`、`customer_id`，支付页面会自动出现**保存卡选项**
4. 支付完成后，通过前端监听事件 / Webhook 订阅 `payment_consent.verified` 事件 / Get list of PaymentConsents 接口获取 `consent_id`
5. 通过 Webhook 订阅支付结果（如 success、fail），或通过 Retrieve a PaymentIntent 接口查询订单状态，形成闭环

**首次绑卡并支付（字段嵌入）：**
1. 后端创建 Customer → 获取 `customer_id`
2. 后端创建 Payment Intent → 传入 `customer_id`
3. 前端集成 card/split-card 的 `createPaymentConsent` 组件，传入 `intent_id`、`client_secret`、`customer_id`，将 `next_triggered_by` 设置为 `customer`
4. 获取 `consent_id` 用于后续支付

**后续支付（HPP/Drop-in）：**
1. 后端创建 Payment Intent → 传入 `customer_id`
2. 前端传入 `intent_id`、`client_secret`、`customer_id`
3. 客户输入 CVC 后完成支付

**后续支付（字段嵌入）：**
1. 后端创建 Payment Intent → 传入 `customer_id`
2. 前端集成 card/split-card 的 confirm 组件和 CVC 输入框，传入 `intent_id`、`client_secret`、`consent_id`
3. 商户需管理好 `consent_id` 和 `customer_id` 的映射关系，以便用户在支付页面选择对应卡号
4. 客户输入 CVC 后完成支付

### 5.6 MIT 模式对接

**首次绑卡并支付：**
1. 后端创建 Customer → 获取 `customer_id`
2. 后端创建 Payment Intent → 传入 `customer_id`
3. 前端设置 `mode: 'recurring'`，并配置 `recurringOptions`
4. 支付完成后，通过前端监听事件 / Webhook 订阅 `payment_consent.verified` / Get list of PaymentConsents 获取 `consent_id`
5. 通过 Webhook 或 Retrieve a PaymentIntent 接口确认支付结果，形成闭环

**仅绑卡（不创建 Payment Intent）：**
1. 后端创建 Customer → 获取 `customer_id` 和 `client_secret`
2. 前端传入 customer 的 `client_secret`（**不传** `intent_id`），设置 `mode: 'recurring'`，配置 `recurringOptions`
3. 客户完成绑卡后，获取 `consent_id` 用于后续支付
4. 后续扣款流程同下方「MIT 后续扣款」

**HPP 模式示例：**

```javascript
payments.redirectToCheckout({
  env: 'demo',
  mode: 'recurring',            // 关键：设为 recurring
  currency: 'USD',
  client_secret: 'xxx',         // intent 或 customer 的 client_secret
  recurringOptions: {
    card: {
      next_triggered_by: 'merchant',        // 关键：MIT 模式
      merchant_trigger_reason: 'scheduled',
      currency: 'USD',
    },
  },
});
```

> **注意：** HPP 模式的 `recurringOptions` 需要按支付方式分组（如 `recurringOptions.card`），而 Drop-in 模式直接在顶层设置 `recurringOptions.next_triggered_by`。

**Drop-in 模式示例：**

```javascript
const dropIn = await window.AirwallexComponentsSDK.createElement('dropIn', {
  intent_id: 'replace-with-your-intent-id',
  client_secret: 'replace-with-your-client-secret',
  currency: 'replace-with-your-currency',
  customer_id: 'replace-with-your-customerid',
  mode: 'recurring',
  recurringOptions: {
    next_triggered_by: 'merchant',
    currency: 'replace-with-your-currency',
  }
});
dropIn.mount('dropIn');
```

**字段嵌入模式示例：**

```javascript
document.getElementById('submit').addEventListener('click', () => {
  Airwallex.createPaymentConsent({
    intent_id: 'int_xxx',          // 可选，传入则是绑卡并支付
    customer_id: 'cus_xxx',        // 必填
    type: 'cardNumber',
    client_secret: 'xxx',
    currency: 'CNY',
    next_triggered_by: 'merchant'  // 'merchant' = MIT, 'customer' = CIT
  }).then((response) => {
    // 获取 consent_id
  });
});
```

> **绑卡模式说明：**
> - 传入 `intent_id` → 使用 intent 的 `client_secret` → **绑卡并支付**
> - 不传 `intent_id` → 使用 customer 的 `client_secret` → **仅绑卡**
>
> **注意：** 字段嵌入模式的循环扣款在正式环境中使用 `https://pci-api.airwallex.com` 域名（而非 `api.airwallex.com`），测试环境使用 `https://api-demo.airwallex.com`。

**获取 consent_id 的三种方式：**
1. 前端监听事件
2. Webhook 订阅 `payment_consent.verified` 事件
3. 调用 Get list of PaymentConsents 接口

**参考文档链接：**
- HPP MIT 示例：https://github.com/airwallex/airwallex-payment-demo/blob/master/integrations/cdn/hpp.html
- Drop-in 注册用户结账：https://www.airwallex.com/docs/payments__drop-in-element__registered-user-checkout
- 字段嵌入循环扣款：https://github.com/airwallex/airwallex-payment-demo/blob/master/docs/recurring.md

#### MIT 后续扣款

```
POST https://api-demo.airwallex.com/api/v1/pa/payment_intents/{id}/confirm
```

```json
{
  "request_id": "13d5a8b9-aa3e-45b7-8a22-6f3ceec8685b",
  "payment_consent_id": "cst_hkdmpspgwfxiesj6ymv"
}
```

**Response 示例：**

```json
{
  "id": "int_3LUABqW4z7kDsG4wazQS28Is1A",
  "request_id": "13d5a8b9-aa3e-45b7-8a22-6f3ceec8685b",
  "amount": 100,
  "currency": "EUR",
  "merchant_order_id": "bdf99a4e-078c-4a4b-b52b-61d1d938b7e6",
  "customer_id": "cus_i2tRw20o4w3vwtZora6cvu9v877",
  "payment_consent_id": "cst_hkdmpspgwfxiesj6ymv",
  "status": "SUCCEEDED",
  "captured_amount": 100,
  "created_at": "2021-04-11T15:48:11+0000",
  "updated_at": "2021-04-11T15:51:34+0000"
}
```

商户可灵活调用 Create Payment Intent + Confirm Payment Intent，改变扣款金额实现定期扣款逻辑。

---

## 6. Google Pay 与 Apple Pay 接入

### 6.1 对比

|  | Google Pay | Apple Pay |
|--|-----------|-----------|
| **集成方式** | HPP、Drop-in、API、Mobile SDK、GooglePay Element | HPP、Drop-in、API、Mobile SDK、ApplePay Element |
| **支持设备** | Android 手机/平板、Chrome、Edge 等浏览器 | Safari 浏览器；原生 App 不受浏览器限制 |
| **前提条件** | 1. Google 账户并激活 Google Pay<br>2. 在 webapp 上激活 | 1. Apple ID 且钱包已添加银行卡<br>2. 在 webapp 上激活并添加域名 |
| **技术限制** | 不支持 WebView 内集成 | 不支持 iframe 内集成 |

### 6.2 Google Pay 对接

1. 在 webapp 后台激活 Google Pay（激活文档：https://www.airwallex.com/docs/payments__global__google-paytm__enable-google-paytm ）
2. 注意：国内 IP 不支持 Google Pay，测试需使用 VPN；Google Pay 不支持在 WebView 场景下使用
3. 前端配置 `googlePayRequestOptions`：

```javascript
googlePayRequestOptions: {
  countryCode: 'US',
  emailRequired: true,
  billingAddressRequired: true,
  billingAddressParameters: {
    format: 'MIN',
    phoneNumberRequired: false
  },
  merchantInfo: {
    merchantName: "Example Merchant",
  },
  buttonType: 'buy',
}
```

**测试说明：** 测试环境需登录真实 Google 账号，可使用 Airwallex 测试卡号（需加入 Google 测试卡套件群组）或真实银行卡（测试环境不会实际扣款）。

### 6.3 Apple Pay 对接

1. 在 webapp 后台激活 Apple Pay（激活文档：https://www.airwallex.com/docs/payments__global__apple-pay__enable-apple-pay-via-web-application__apple-pay-for-web ）
2. **在 webapp 上添加域名要求：**
   - 与开通支付方式时登记的域名一致
   - 需公网可访问
   - 需 HTTPS 协议
3. 前端配置 `applePayRequestOptions`：

```javascript
applePayRequestOptions: {
  countryCode: 'US',
  requiredBillingContactFields: ['postalAddress'],
  requiredShippingContactFields: ['name', 'email'],
  totalPriceLabel: "Your Merchant Name",
  buttonType: 'buy',
  buttonColor: 'white-with-line',
}
```

**测试说明：** Apple Pay 仅可在 Safari 浏览器中展示和测试，需使用已开通 Apple Pay 的真实 Apple 账号（测试环境不会实际扣款）。请核查测试用户所属的国家/地区是否支持 Apple Pay。

### 6.4 HPP / Drop-in 钱包参数完整示例

**HPP 模式：**

```javascript
payments.redirectToCheckout({
  intent_id: intent.id,
  client_secret: intent.client_secret,
  currency: 'intent.currency',
  applePayRequestOptions: {
    buttonType: 'buy',
    buttonColor: 'white-with-line',
    countryCode: 'HK',
    totalPriceLabel: 'COMPANY, INC.'
  },
  googlePayRequestOptions: {
    countryCode: 'HK',
    merchantInfo: { merchantName: 'Example Merchant' },
    emailRequired: true,
    billingAddressRequired: true,
    buttonType: 'book',
    buttonColor: 'black',
    buttonSizeMode: 'fill'
  }
});
```

文档链接：https://www.airwallex.com/docs/payments__global__google-paytm__hosted-payment-page

**Drop-in 模式：**

```javascript
const dropInElement = createElement('dropIn', {
  intent_id: intent.id,
  client_secret: intent.client_secret,
  currency: 'intent.currency',
  applePayRequestOptions: {
    countryCode: 'US',
    buttonType: 'buy',
    buttonColor: 'white-with-line',
  },
  googlePayRequestOptions: {
    countryCode: 'US',
    merchantInfo: { merchantName: 'Example Merchant' },
    buttonType: 'buy',
  }
});
```

文档链接：https://www.airwallex.com/docs/payments__global__apple-pay__drop-in-element

---

## 7. 退款处理

### 7.1 创建退款

```
POST https://api-demo.airwallex.com/api/v1/pa/refunds/create
```

```json
{
  "payment_intent_id": "int_eiyDfBGLz2dUsAadJzikN0eKrCp",
  "payment_attempt_id": "att_4rR5bWI3z9dVl6R7gzikN0eKrCp",
  "reason": "Return good",
  "amount": 300,
  "request_id": "2ef2dbf9-0568-472a-a76d-6420dc10581f"
}
```

> `payment_intent_id` 和 `payment_attempt_id` 任选其一即可。不指定金额则**全额退款**。

### 7.2 退款状态流转

| 状态 | 说明 |
|-----|------|
| **RECEIVED** | 退款请求已收到，稍后处理 |
| **ACCEPTED** | 发卡行/钱包已成功受理，到账时间以实际为准 |
| **SUCCEEDED** | 退款完成 |
| **FAILED** | 退款失败（通常在受理阶段） |

**消费者侧状态处理建议：**
1. 成功创建 refund 记录 → 显示「正在处理中...」
2. 收到 `Refund - SUCCEEDED` → 显示「退款成功」；收到 `Refund - FAILED` → 显示「退款失败」
3. 可选：订阅 `Refund - Accepted` → 提示「退款已成功受理，到账时间以钱包为准」

> **API 版本注意：**
> - 2021-08-06 之前，`Refund - Accepted` 叫做 `Refund - PROCESSING`
> - 2025-02-14 之后，`refund.succeeded` 改为 `refund.settled`

### 7.3 退款注意事项

- 退款沿支付路径**原路退回**
- 支持**部分退款**和**多次退款**，总额不得超过原消费金额
- 对于卡支付，退款的执行时间周期（结算周期）**与消费交易的请款一致**
- 退款需满足资金要求：
  1. 待结算资金 > 退款金额，或
  2. 交易币种钱包余额 > 退款金额，或
  3. 待结算资金 + 交易币种钱包余额 > 退款金额
- 当交易货币与结算货币不同时，会计算换汇后金额

---

## 8. Webhook 订阅与配置

### 8.1 建议订阅的事件

| 类别 | 事件 | 说明 |
|-----|------|------|
| **交易订单** | Payment Intent - Succeeded | 支付成功时触发 |
| **交易请求** | Payment Attempt - Authorization Failed | 授权失败时触发 |
| | Payment Attempt - Authentication Failed | 3DS 验证失败时触发 |
| | Payment Attempt - Capture Failed | 请款失败时触发 |
| **退款** | Refund - Received | 退款请求创建成功 |
| | Refund - Accepted | 退款请求已受理 |
| | Refund - Succeeded | 退款成功 |
| | Refund - Failed | 退款失败 |
| **拒付** | Dispute 相关事件 | 拒付通知 |

> 登录 Airwallex 账户 → 账户 → 开发者 → Webhooks 设置订阅。处理以上事件是**上线检查清单**中的主要一项。

### 8.2 配置注意事项

1. 默认最多 **2 个接收地址**，增加需联系客户经理
2. 仅支持 **HTTPS** 接收地址（Demo 环境也要求 HTTPS）
3. 需在 **10 秒内** 返回 HTTP 200，建议接收逻辑和处理逻辑分开
4. **重发机制：** 失败后间隔 5 分钟 → 1 小时 → 4 小时 → 8 小时 → 12 小时 → 12 小时，共重发 6 次
5. 接收时检查 `id` 字段确保**不重复处理**，检查 `created_at` 确认消息顺序

### 8.3 Webhook 验签

- 在开发者 → Webhooks 位置获取 Webhook 密钥
- **必须先返回 HTTP 200 再验签**，否则 Airwallex 会认为发送失败重发，导致 timestamp 不同验签失败
- 如无法验签，可按文档添加空中云汇的 IP 白名单
- 未收到回调通知时，可在 Events 下勾选对应事件点击**重新触发**

---

## 9. 风控字段传入

### 9.1 虚拟行业（游戏、直播等）

```json
{
  "additional_info": {
    "customer_activity_data": {
      "registration_date": "2019-09-18",
      "registration_ip_address": "212.121.222.123"
    }
  },
  "customer": {
    "address": {
      "city": "Shanghai",
      "country_code": "CN",
      "postcode": "100000",
      "state": "Shanghai",
      "street": "Pudong District"
    },
    "business_name": "Abc Trading Limited",
    "email": "john.doe@airwallex.com",
    "first_name": "John",
    "last_name": "Doe",
    "merchant_customer_id": "user_id_123",
    "phone_number": "13800000000"
  },
  "order": {
    "products": [{
      "code": "3414314111",
      "desc": "产品描述",
      "name": "产品名称",
      "quantity": 5,
      "sku": "100004",
      "type": "physical",
      "unit_price": 100.01,
      "url": "https://example.com/product/12345"
    }]
  }
}
```

### 9.2 实物交易（快消、家具、电子产品等）

在虚拟行业字段基础上，额外传入 `shipping` 信息：

```json
"shipping": {
  "address": {
    "city": "Shanghai",
    "country_code": "CN",
    "postcode": "100000"
  },
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "13800000000"
}
```

> **字段优先级：** 红色 = 必传 | 紫色 = 建议传输 | 黄色 = 可选
>
> **注意：** 非直连模式（HPP/Drop-in）下，billing 字段需在前端 JS 中完成传递（通过 `withBilling: true` 和 `requiredBillingContactFields` 参数）。字段嵌入模式下，billing 信息需在 `confirmPaymentIntent` 调用中通过 `payment_method.billing` 对象传入：

```javascript
Airwallex.confirmPaymentIntent({
  element: Airwallex.getElement('cardNumber'),
  intent_id: 'your-intentid',
  client_secret: 'your-client-secret',
  currency: 'your-currency',
  payment_method: {
    billing: {
      email: 'xxx@test.com',
      first_name: 'Test',
      last_name: 'Test',
      date_of_birth: '1990-01-01',
      phone_number: '13999999999',
      address: {
        city: 'Shanghai',
        country_code: 'CN',
        postcode: '201000',
        state: 'Shanghai',
        street: 'test road'
      }
    }
  }
});
```

---

## 10. 自动货币兑换

使用全托管页面对接时，商户可在 webapp 后台开启**自动币种兑换功能**。

- 商户创建订单时使用单一币种
- 消费者支付时自行选择支持的支付币种
- 目前支持 **26 个币种**自动兑换

**不支持的场景：**
1. 订阅管理
2. 多币种定价的商品
3. 手动请款的交易
4. 平台类型的交易

详见：https://www.airwallex.com/docs/payments__automatic-currency-conversion

---

## 11. 测试与上线

### 11.1 测试卡号

| 用例 | 测试卡号 | 预期结果 |
|-----|---------|---------|
| 支付成功（无 3DS） | `4012000300000021` | Frictionless Mode Success (200 OK) |
| 支付成功（有 3DS） | `4012000300000088`，OTP：`1234` | Challenge Mode Success (200 OK) |
| 3DS 验证失败 | `4012000300000013` | `authentication_declined` |
| 3DS 验证失败 | `4012000300000039` | `authentication_declined` |
| 3DS 验证失败 | `4012000300000070` | `authentication_declined` |
| 授权失败 | `4012000300000021`，金额 `88.88` | `issuer_declined` (provider_original_response_code: "01") |
| 授权失败 | `4012000300000088`，金额 `88.88` | `issuer_declined` (provider_original_response_code: "01") |

> CVC/CVV 和有效期可填任意值。更多测试卡：https://www.airwallex.com/docs/payments__test-card-numbers
> 测试样例：https://www.airwallex.com/docs/payments__integration-checklist

### 11.2 支付失败错误码与建议话术

#### 非发卡行错误

| code | 原因 | 建议话术 |
|------|------|---------|
| `validation_error` (invalid pan) | 卡号无效 | 卡号或账户无效，请核实所有信息无误后重试 |
| `card_brand_not_supported` | 卡品牌不支持 | 卡号或账户无效，请核实所有信息无误后重试 |
| `risk_declined` | Airwallex 风控拒绝 | 支付失败，请尝试使用其他银行卡或其他支付方式 |
| `authentication_decline` | 3DS 认证失败 | 交易认证失败，请检查支付信息后重试，或选择其他支付方式 |

#### 发卡行错误 (`issuer_declined`)

| provider_original_response_code | 原因 | 建议话术 |
|--------------------------------|------|---------|
| 12, 06 | 未知错误/没有响应 | 无法确认卡信息。请尝试使用其他银行卡或支付方式。如持续出现，请提供错误截图和订单号进一步核查。 |
| 51, 61 | 余额不足/超过消费限制 | 余额不足或超出信用额度，请使用其他银行卡或其他支付方式重试。 |
| 82 | CVV 安全验证码错误 | CVC/CVC2（安全码）无效，请检查后重试。 |
| 54 | 卡过期 | 银行卡已过期或您输入的有效期不正确。请检查后重试或尝试使用其他银行卡。 |
| 63, 93, 05, 57 | 通用发卡行拒绝/未授权 | 发卡行拒绝了本次交易。请尝试其他银行卡或使用其他支付方式。如需确认，请联系发卡行。 |
| 14, 15 | 卡号无效 | 卡号或账户无效，请核实所有信息无误后重试。 |
| 91 | 发生临时错误 | 授权过程中发生临时错误，请重试。如持续出现，请联系发卡行。 |
| 41, 07 | 欺诈卡/受限卡 | 信用卡存在一些限制，发卡行已拒绝本次交易。请使用其他银行卡重试。如需确认，请联系发卡行。 |
| 59 | 银行风控导致交易失败 | 无法确认卡信息。请尝试使用其他银行卡或支付方式。如需帮助，请联系发卡行。 |
| 79 | 请稍后重试 | 无法确认卡信息。请使用其他银行卡或其他支付方式重试。 |
| 78 | 未激活卡 | 该银行卡未激活，请激活后再试。 |
| 13 | 无效金额 (invalid amount) | 无法处理付款。请检查您的支付信息后重试，或选择其他支付方式。 |

#### 卡交易失败的分类提示

当消费者支付失败时，依据 `provider_original_response_code` 分为两类：

| 分类 | 对应码 | 处理方式 |
|-----|--------|---------|
| **输入信息有误，可修正** | 14, 15, 30（卡号错误）；82, 89, N7（CVV 错误）；51, 61（余额不足） | 提示消费者修正信息后重试 |
| **不可修正** | 其他所有 code | 提示消费者换卡重试 |

### 11.3 上线检查清单

| 检查项目 | 说明 | 责任方 |
|---------|------|--------|
| Webhook: Payment Intent Succeeded | 确保订阅了支付成功事件 | 商户 + AWX |
| Webhook: Authorization Failed | 确保订阅了授权失败事件 | 商户 + AWX |
| Webhook: Authentication Failed | 确保订阅了验证失败事件 | 商户 + AWX |
| API: Retrieve Payment Intent | 确保调用了查询支付状态的接口 | 商户 + AWX |
| Webhook: Refund Received | 确保订阅了创建退款事件 | 商户 + AWX |
| Webhook: Refund Succeeded | 确保订阅了退款成功事件 | 商户 + AWX |
| Webhook: Refund Failed | 确保订阅了退款失败事件 | 商户 + AWX |
| Notify URL | 确保使用生产环境 URL，且为 HTTPS | 商户 |

### 11.4 上线步骤

1. 确认完成测试样例：https://www.airwallex.com/docs/payments__integration-checklist
2. API 地址从 `https://api-demo.airwallex.com` 切换为 `https://api.airwallex.com`
3. 前端 `env` 从 `demo` 改为 `prod`
4. 替换为生产账号的 Client ID 和 API Key

> **重要：** 请勿直接在生产环境进行开发测试，生产环境交易会产生手续费。

---

## 12. 附录

### 12.1 各种 ID 汇总

| 名称 | 说明 |
|-----|------|
| **Client ID** | 从账户后台获取，与 API Key 一起获取访问令牌 |
| **Request ID** | 商户系统生成，调用"写"操作的 API 时传入，**必须唯一** |
| **Intent ID** | 支付订单标识，对应商户的商品订单 |
| **Attempt ID** | 终端用户某一次支付请求，由 Airwallex 自动创建，与 Intent ID 是多对一关系 |

### 12.2 各种有效期汇总

| 名称 | 有效期 | 实施要求 |
|-----|--------|---------|
| **Access Token** | 创建后 30 分钟 | 缓存 Token，20 分钟后重新获取 |
| **Intent Client Secret** | 1 小时 | 确保用户在 1 小时内使用；如需刷新，调用 Retrieve PaymentIntent 获取新的 |
| **Attempt Valid Time** | 2 小时 | 确保商户系统实现有效期异常处理 |

### 12.3 Payment Intent 状态说明

| 交易状态（webapp） | PI 状态（API/Webhook） | 说明 |
|-------------------|----------------------|------|
| Created / Failed | `REQUIRES_PAYMENT_METHOD` | 订单刚创建或支付失败 |
| Pending | `REQUIRES_CUSTOMER_ACTION` | 需持卡人完成 3DS 认证（临时状态） |
| Authorized | `REQUIRES_CAPTURE` | 已授权，准备请款 |
| Succeeded | `SUCCEEDED` | 支付成功 |
| Canceled | `CANCELLED` | 商户已终止支付 |
| Disputed | `DISPUTED` | 用户提出拒付 |
| Refunded | `SUCCEEDED` | 退款不改变 Intent 状态 |

> 查询失败原因：通过 Retrieve Intent 接口返回的 `latest_payment_attempt.failure_code` 判断。

### 12.4 主要 API 清单

| API | 用途 | 必要性 |
|-----|------|--------|
| **Obtain Access Token** | 获取 API 访问令牌 | 必选 |
| **Create a PaymentIntent** | 创建支付订单 | 必选 |
| **Retrieve a PaymentIntent** | 查询支付订单详情 | 必选 |
| **Get list of PaymentIntents** | 获取所有支付订单列表 | 可选 |
| **Create a Customer** | 创建客户对象（CIT/MIT 场景） | 可选 |
| **Disable a PaymentConsent** | 使 consent_id 失效 | 可选 |
| **Get list of PaymentConsents** | 查询 consent_id | 可选 |
| **Create a Refund** | 创建退款 | 可选 |
| **Get list of Refunds / Retrieve a Refund** | 查询退款记录 | 可选 |
| **Capture a PaymentIntent** | 手动请款 | 可选 |
| **Cancel a PaymentIntent** | 取消支付订单 | 可选 |
| **Get balance history** | 余额流水报告 | 可选 |
| **Get list of financial transactions** | 交易记录报告 | 可选 |
| **Get list of settlements** | 收单结算报告 | 可选 |

### 12.5 PCI DSS 合规

PCI DSS 是面向所有存储、处理或传输持卡人数据和/或敏感验证数据的所有实体的全球性安全标准。根据支付集成方式可选择不同的 SAQ 类别，**是上线前必须提供的文件**：

| 对接方式 | 证书要求 |
|---------|---------|
| 托管页面模式 | SAQ-A 文件 |
| 模块嵌入模式 | SAQ-A 文件 |

文档下载：https://www.pcisecuritystandards.org/document_library?category=saq&document=saq

### 12.6 错误响应字段说明

| 字段 | 说明 |
|-----|------|
| `code` | 失败类型 |
| `message` | 错误提示消息 |
| `provider_original_response_code` | 当 code 为 `provider_declined` 或 `issuer_declined` 时，说明授权失败的原因 |
| `source` | 请求中存在问题的字段 |

**文档地址：**
- 失败返回响应：https://www.airwallex.com/docs/online-payments__native-api__error-response-codes
- 发卡行返回码：https://www.airwallex.com/docs/online-payments__response-codes__issuer-response-codes
