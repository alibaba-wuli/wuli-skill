# 呜哩 Wuli 开放平台 API 文档

## 概述

呜哩开放平台提供图片生成、视频生成等 AI 能力的 API 接口，支持通过 API Token 进行身份认证。

*   **服务地址**: \`https://platform.wuli.art/api/v1/\`
    
*   **认证方式**: 所有平台接口通过请求头 `Authorization: Bearer <API Token>` 传递 API Token 进行身份认证
    
*   **积分消耗**: API 调用正常消耗积分，积分明细中以"API调用-"为前缀标记
    
*   **数据隔离**: 通过 API 提交的任务不会出现在网页端的历史记录和资源库中
    

---

## 认证

### 获取 API Token

登录 [wuli.art](https://wuli.art)，在左下角进入「API 开放平台」入口，查看或重置你的访问令牌。

也可以通过以下接口管理 Token（需先通过网页端登录）：

#### 获取 Token

```plaintext
GET /api/v1/user/getApiToken
```

**响应示例：**

```plaintext
{
  "success": true,
  "code": 200,
  "data": {
    "apiToken": "wuli-a1b2c3d4e5f6..."
  }
}
```

#### 生成/重置 Token

```plaintext
POST /api/v1/user/genApiToken
```

**响应示例：**

```plaintext
{
  "success": true,
  "code": 200,
  "data": {
    "apiToken": "wuli-a1b2c3d4e5f6..."
  }
}
```
> 重置后旧 Token 立即失效。

### 认证方式

在所有平台 API 请求中，通过请求头传递 Token：

```plaintext
Authorization: Bearer wuli-a1b2c3d4e5f6...
```
---

## 通用响应格式

所有接口响应均遵循以下格式：

```plaintext
{
  "success": true,
  "code": 200,
  "msg": "成功",
  "data": { ... },
  "requestId": "xxx"
}
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| success | boolean | 请求是否成功 |
| code | int | 状态码，200 为成功 |
| msg | string | 错误信息 |
| data | object | 响应数据 |
| requestId | string | 请求追踪 ID |

---

## 接口列表

### 1. 提交生图/视频任务

```plaintext
POST /api/v1/platform/predict/submit
```

提交一个图片或视频生成任务。任务为异步执行，提交后通过查询接口轮询结果。

#### 请求头

| Header | 必填 | 说明 |
| --- | --- | --- |
| Authorization | 是 | `Bearer <API Token>` |
| Content-Type | 是 | application/json |

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| modelName | string | 是 | 模型名称，见下方[可用模型列表](#可用模型) |
| prompt | string | 是 | 提示词，最长 2000 字符 |
| mediaType | string | 否 | 媒体类型：`IMAGE` 或 `VIDEO`，不传则根据模型自动判断 |
| predictType | string | 否 | 生成类型，不传则自动推断。详见[生成类型说明](#生成类型) |
| aspectRatio | string | 是 | 画面比例，如 `1:1`、`16:9`、`9:16` 等 |
| resolution | string | 是 | 分辨率，如 `2K`、`4K`（图片）或 `720P`、`1080P`（视频） |
| n | int | 否 | 生成数量，1-4，默认 1 |
| inputImageList | array | 否 | 参考图片列表，用于图生图/图生视频 |
| inputVideoList | array | 否 | 参考视频列表，用于视频生视频 |
| videoTotalSeconds | int | 否 | 视频时长（秒），仅视频模型有效，默认 5 |
| negativePrompt | string | 否 | 反向提示词 |
| seed | int | 否 | 随机种子，默认 -1（随机） |
| optimizePrompt | boolean | 否 | 是否优化提示词，默认 false |

**inputImageList / inputVideoList 中每个元素格式：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| imageUrl | string | 图片/视频的 URL（须通过上传接口获取） |

#### 请求示例

**文生图：**

```plaintext
{
  "modelName": "Qwen Image Turbo",
  "prompt": "一只穿着太空服的猫咪在月球上漫步，背景是蓝色地球",
  "mediaType": "IMAGE",
  "aspectRatio": "1:1",
  "resolution": "2K",
  "n": 4,
  "optimizePrompt": true
}
```

**图生图：**

```plaintext
{
  "modelName": "Qwen Image 2.0",
  "prompt": "将这张照片变成水彩画风格",
  "mediaType": "IMAGE",
  "predictType": "REF_2_IMG",
  "aspectRatio": "16:9",
  "resolution": "2K",
  "n": 2,
  "inputImageList": [
    { "imageUrl": "https://your-uploaded-image-url.jpg" }
  ]
}
```

**文生视频：**

```plaintext
{
  "modelName": "通义万相 2.2 Turbo",
  "prompt": "海浪拍打着金色的沙滩，夕阳西下",
  "mediaType": "VIDEO",
  "aspectRatio": "16:9",
  "resolution": "720P",
  "videoTotalSeconds": 5
}
```

**图生视频：**

```plaintext
{
  "modelName": "通义万相 2.6",
  "prompt": "让画面中的花朵缓缓绽放",
  "mediaType": "VIDEO",
  "predictType": "FF_2_VIDEO",
  "aspectRatio": "16:9",
  "resolution": "720P",
  "videoTotalSeconds": 5,
  "inputImageList": [
    { "imageUrl": "https://your-uploaded-image-url.jpg" }
  ]
}
```

#### 响应参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| recordId | string | 任务记录 ID，用于后续查询 |
| credit | object | 积分消耗信息 |
| credit.modelGroup | string | 模型分组名 |
| credit.previousFreeUsage | int | 消耗前剩余免费次数 |
| credit.currentFreeUsage | int | 消耗后剩余免费次数 |

#### 响应示例

```plaintext
{
  "success": true,
  "code": 200,
  "data": {
    "recordId": "01JWXYZ...",
    "credit": {
      "modelGroup": "IMAGE_DEFAULT",
      "previousFreeUsage": 10,
      "currentFreeUsage": 6
    }
  }
}
```
---

### 2. 查询任务状态

```plaintext
GET /api/v1/platform/predict/query?recordId={recordId}
```

根据 `recordId` 查询任务状态和生成结果。建议以 2-5 秒间隔轮询，直到状态为终态。

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| recordId | string | 是 | 提交任务时返回的记录 ID |

#### 响应参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| recordId | string | 记录 ID |
| recordStatus | string | 任务整体状态，见[任务状态说明](#任务状态) |
| gmtCreate | string | 创建时间 |
| mediaType | string | `IMAGE` 或 `VIDEO` |
| modelInfo | object | 模型信息 |
| modelInfo.modelName | string | 模型名称 |
| genInfo | object | 生成参数信息 |
| genInfo.prompt | string | 提示词 |
| genInfo.predictType | string | 生成类型 |
| genInfo.aspectRatio | string | 画面比例 |
| genInfo.resolution | string | 分辨率 |
| genInfo.width | int | 宽度（像素） |
| genInfo.height | int | 高度（像素） |
| genInfo.videoTotalSeconds | int | 视频时长（秒） |
| results | array | 生成结果列表 |
| results\[\].taskId | string | 子任务 ID |
| results\[\].imageId | string | 资源 ID |
| results\[\].imageUrl | string | 结果图片/视频 URL（带水印） |
| results\[\].status | string | 子任务状态 |
| results\[\].progress | int | 进度百分比 |
| results\[\].errorMsg | string | 错误信息 |
| results\[\].star | int | 收藏状态 |

#### 响应示例

```plaintext
{
  "success": true,
  "code": 200,
  "data": {
    "recordId": "01JWXYZ...",
    "recordStatus": "SUCCEED",
    "gmtCreate": "2026-03-11T10:30:00.000+08:00",
    "mediaType": "IMAGE",
    "modelInfo": {
      "modelName": "Qwen Image Turbo"
    },
    "genInfo": {
      "prompt": "一只穿着太空服的猫咪在月球上漫步",
      "predictType": "TXT_2_IMG",
      "aspectRatio": "1:1",
      "resolution": "2K",
      "width": 1024,
      "height": 1024,
      "optimizePrompt": true
    },
    "results": [
      {
        "taskId": "01JWABC...",
        "imageId": "01JWDEF...",
        "imageUrl": "https://cdn.wuli.art/result/xxx.png",
        "status": "SUCCEED",
        "progress": 100,
        "star": 0
      }
    ]
  }
}
```
---

### 3. 获取无水印图片/视频

```plaintext
POST /api/v1/platform/predict/noWatermarkImage
```

获取生成结果的无水印版本 URL。

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| taskId | string | 否\* | 子任务 ID |
| resourceId | string | 否\* | 资源 ID |
| resourceIdList | array | 否\* | 资源 ID 列表（批量获取） |

> \*三个参数至少传一个。

#### 请求示例

```plaintext
{
  "taskId": "01JWABC..."
}
```

或批量获取：

```plaintext
{
  "resourceIdList": ["01JWDEF...", "01JWGHI..."]
}
```

#### 响应示例

```plaintext
{
  "success": true,
  "code": 200,
  "data": {
    "url": "https://cdn.wuli.art/result/xxx_nowatermark.png",
    "urlList": [
      "https://cdn.wuli.art/result/xxx1_nowatermark.png",
      "https://cdn.wuli.art/result/xxx2_nowatermark.png"
    ]
  }
}
```
---

### 4. 获取预签名上传 URL

```plaintext
GET /api/v1/platform/image/getUploadUrl?filename={filename}
```

获取 OSS 预签名上传 URL，用于上传参考图片或视频。上传成功后，将 `uploadUrl` 去掉签名参数后的公网 URL 用作 `inputImageList` / `inputVideoList` 中的 `imageUrl` 字段值。

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| filename | string | 是 | 文件名（含后缀），如 `photo.jpg`、`clip.mp4` |

支持的图片格式：`jpg`、`jpeg`、`png`、`webp` 支持的视频格式：`mp4`、`mov`、`avi`、`webm`

#### 响应参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| uploadUrl | string | 预签名上传 URL，使用 `PUT` 方法上传文件，有效期 1 小时 |
| objectName | string | 文件对象名（仅供参考） |

#### 响应示例

```plaintext
{
  "success": true,
  "code": 200,
  "data": {
    "uploadUrl": "https://oss.aliyuncs.com/wuli/xxx?签名参数...",
    "objectName": "upload/2026/03/11/abc123.jpg"
  }
}
```

#### 使用流程

1.  调用本接口获取 `uploadUrl` 和 `objectName`
    
2.  使用 `PUT` 方法将文件上传到 `uploadUrl`
    
3.  将 `uploadUrl` 去掉查询参数（`?Expires=...` 部分）后的公网 URL 作为 `inputImageList[].imageUrl` 的值传入生成接口
    

---

## 可用模型

### 图片生成模型

| 模型名称 (modelName) | 支持的生成类型 | 支持的分辨率 | 最大生成数 | 最大参考图数 | 每张积分消耗 |
| --- | --- | --- | --- | --- | --- |
| Qwen Image 2.0 | TXT_2_IMG, REF_2_IMG | 2K, 4K | 4 | 4 | 1 |
| Qwen Image Turbo | TXT_2_IMG, REF_2_IMG | 2K, 4K | 4 | 4 | 1 |
| Qwen Image 25.08 | TXT_2_IMG | 2K, 4K | 4 | 0 | 1 |
| Seedream 4.5 | TXT_2_IMG, REF_2_IMG | 2K, 4K | 4 | 8 | 4 |
| Seedream 4.0 | TXT_2_IMG, REF_2_IMG | 1K, 2K, 4K | 4 | 8 | 4 |
| 通义万相 2.6 | TXT_2_IMG, REF_2_IMG | 1K | 1 | 4 | 4 |

#### 图片画面比例

| aspectRatio | 说明 |
| --- | --- |
| 1:1 | 正方形 |
| 4:3 | 横向 4:3 |
| 3:2 | 横向 3:2 |
| 16:9 | 宽屏横向 |
| 21:9 | 超宽横向 |
| 3:4 | 纵向 3:4 |
| 2:3 | 纵向 2:3 |
| 9:16 | 竖屏纵向 |
| 9:21 | 超高纵向 |

---

### 视频生成模型

| 模型名称 (modelName) | 支持的生成类型 | 支持的分辨率 | 支持的时长(秒) | 最大参考图数 |
| --- | --- | --- | --- | --- |
| 通义万相 2.2 Turbo | TXT_2_VIDEO, FF_2_VIDEO | 720P | 5 | 1 |
| 通义万相 2.6 | TXT_2_VIDEO, FF_2_VIDEO, MULTI_IMG_2_VIDEO, VIDEO_2\_VIDEO | 720P, 1080P | 5, 10, 15 | 5 |
| 通义万相 2.6 Flash | FF_2_VIDEO | 720P, 1080P | 5, 10, 15 | 1 |
| 可灵 O1 | TXT_2_VIDEO, FF_2_VIDEO, FLF_2_VIDEO, MULTI_IMG_2_VIDEO, VIDEO_2\_VIDEO | 720P, 1080P | 5, 10 | 7 |
| 可灵 2.6 | TXT_2_VIDEO, FF_2_VIDEO, FLF_2_VIDEO | 1080P | 5, 10 | 2 |
| 可灵 2.5 Turbo | TXT_2_VIDEO, FF_2_VIDEO, FLF_2_VIDEO | 720P, 1080P | 5, 10 | 2 |
| Seedance 1.5 Pro | TXT_2_VIDEO, FF_2_VIDEO, FLF_2_VIDEO | 480P, 720P | 5, 10, 12 | 2 |
| Seedance 1.0 Pro | TXT_2_VIDEO, FF_2_VIDEO, FLF_2_VIDEO | 480P, 720P, 1080P | 5, 10 | 2 |
| MiniMax Hailuo 2.3 | TXT_2_VIDEO, FF_2_VIDEO | 768P, 1080P | 6, 10 | 1 |
| MiniMax Hailuo 2.3 Fast | FF_2_VIDEO | 768P, 1080P | 6, 10 | 1 |

#### 视频积分消耗

视频积分根据分辨率和时长不同而不同，以下为各模型积分参考：

**通义万相 2.2 Turbo**

| 分辨率 | 5秒 | 10秒 |
| --- | --- | --- |
| 720P | 20 | 40 |

**通义万相 2.6**

| 分辨率 | 5秒 | 10秒 | 15秒 |
| --- | --- | --- | --- |
| 720P | 40 | 80 | 120 |
| 1080P | 60 | 120 | 180 |

**通义万相 2.6 Flash**

| 分辨率 | 5秒 | 10秒 | 15秒 |
| --- | --- | --- | --- |
| 720P | 20 | 40 | 60 |
| 1080P | 40 | 80 | 120 |

**可灵 O1**

| 分辨率 | 5秒 | 10秒 |
| --- | --- | --- |
| 720P | 40 | 80 |
| 1080P | 60 | 100 |

> 可灵 O1 的 VIDEO_2_VIDEO 模式积分更高（720P: 60/120, 1080P: 80/160）

**可灵 2.6**

| 分辨率 | 5秒 | 10秒 |
| --- | --- | --- |
| 1080P | 60 | 120 |

**可灵 2.5 Turbo**

| 分辨率 | 5秒 | 10秒 |
| --- | --- | --- |
| 1080P | 40 | 80 |

**Seedance 1.5 Pro**

| 分辨率 | 5秒 | 10秒 | 12秒 |
| --- | --- | --- | --- |
| 480P | 20 | 40 | 60 |
| 720P | 40 | 80 | 100 |

**Seedance 1.0 Pro**

| 分辨率 | 5秒 | 10秒 |
| --- | --- | --- |
| 480P | 20 | 40 |
| 720P | 40 | 80 |
| 1080P | 80 | 160 |

**MiniMax Hailuo 2.3**

| 分辨率 | 6秒 | 10秒 |
| --- | --- | --- |
| 768P | 40 | 80 |
| 1080P | 60 | 120 |

**MiniMax Hailuo 2.3 Fast**

| 分辨率 | 6秒 | 10秒 |
| --- | --- | --- |
| 768P | 20 | 40 |
| 1080P | 40 | 80 |

#### 视频画面比例

| aspectRatio | 说明 |
| --- | --- |
| 1:1 | 正方形 |
| 4:3 | 横向 4:3 |
| 3:4 | 纵向 3:4 |
| 16:9 | 宽屏横向 |
| 9:16 | 竖屏纵向 |

> 不同模型支持的画面比例可能不同，请以实际模型配置为准。

---

## 生成类型

| predictType | 说明 | 适用场景 |
| --- | --- | --- |
| TXT_2_IMG | 文生图 | 纯文本提示词生成图片 |
| REF_2_IMG | 图生图 | 参考图片 + 提示词生成图片 |
| TXT_2_VIDEO | 文生视频 | 纯文本提示词生成视频 |
| FF_2_VIDEO | 图生视频（首帧） | 单张参考图 + 提示词生成视频 |
| FLF_2_VIDEO | 图生视频（首尾帧） | 首尾两张参考图 + 提示词生成视频 |
| MULTI_IMG_2\_VIDEO | 多图生视频 | 多张参考图 + 提示词生成视频 |
| VIDEO_2_VIDEO | 视频生视频 | 参考视频 + 提示词生成视频 |

---

## 任务状态

| 状态 (status) | 说明 | 是否终态 |
| --- | --- | --- |
| INITIALIZING | 初始化中 | 否 |
| OPTIMIZING | 提示词优化中 | 否 |
| PENDING | 排队等待中 | 否 |
| PROCESSING | 生成中 | 否 |
| SUCCEED | 生成成功 | 是 |
| FAILED | 生成失败 | 是 |
| REVIEW\_FAILED | 内容审核不通过 | 是 |
| TIMEOUT | 任务超时 | 是 |
| CANCELLED | 已取消 | 是 |

---

## 错误码

| code | 说明 |
| --- | --- |
| 200 | 成功 |
| 401 | 未认证，Token 无效或缺失 |
| 403 | 无权限 |
| 429 | 请求频率过高 |
| 1001 | 参数错误 |
| 2001 | 积分余额不足 |
| 5000 | 服务内部错误 |

---

## 典型调用流程

```plaintext
1. 上传参考素材（如需要）
   GET /api/v1/platform/image/getUploadUrl?filename=ref.jpg
   → PUT 上传文件到返回的 uploadUrl（需加 Content-Type: application/octet-stream 请求头）
   → 将 uploadUrl 去掉签名参数后的公网 URL 作为图片/视频引用
2. 提交生成任务
   POST /api/v1/platform/predict/submit
   → 获得 recordId

3. 轮询任务状态（建议间隔 2~5 秒）
   GET /api/v1/platform/predict/query?recordId=xxx
   → 直到 recordStatus 为终态 (SUCCEED / FAILED / ...)

4. 获取无水印结果（可选）
   POST /api/v1/platform/predict/noWatermarkImage
   → 获得无水印 URL
```