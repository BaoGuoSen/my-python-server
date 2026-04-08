# Home Cook 接口文档

**Base URL**: `http://127.0.0.1:8000`
**Content-Type**: `application/json`

---

## 认证说明

需要登录的接口，请在请求头中携带 Token：

```
Authorization: Bearer <access_token>
```

Token 通过微信登录接口获取，有效期 **7 天**。

---

## 错误响应格式

```json
{
  "detail": "错误描述"
}
```

| HTTP 状态码 | 说明 |
|---|---|
| 400 | 请求参数错误 |
| 401 | 未登录或 Token 无效 |
| 403 | 无权限（非 Owner） |
| 404 | 资源不存在 |
| 422 | 字段校验失败 |

---

## 一、认证模块

### 1.1 微信登录

**POST** `/api/auth/wx-login`

无需 Token。用微信 `wx.login()` 拿到的 `code` 换取系统 Token。

**Request Body**

```json
{
  "code": "wx_auth_code_from_wx.login",
  "nickname": "张三",
  "avatar_url": "https://example.com/avatar.jpg"
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| code | string | ✅ | 微信 wx.login() 返回的 code |
| nickname | string | ✅ | 用户昵称，来自 wx.getUserProfile() |
| avatar_url | string | ✅ | 用户头像地址，来自 wx.getUserProfile() |

**Response 200**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "nickname": "张三",
  "avatar_url": "https://example.com/avatar.jpg"
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| access_token | string | JWT Token，后续请求放入 Header |
| token_type | string | 固定值 "bearer" |
| user_id | number | 用户 ID |
| nickname | string | 用户昵称 |
| avatar_url | string | 用户头像地址 |

---

## 二、用户模块

### 2.1 获取当前用户信息

**GET** `/api/users/me`

需要 Token。

**Response 200**

```json
{
  "id": 1,
  "open_id": "oXXXXXXXXXXXXXXX",
  "nickname": "张三",
  "avatar_url": "https://example.com/avatar.jpg",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

### 2.2 更新用户信息

**POST** `/api/users/me/update`

需要 Token。字段均为可选，只传需要修改的字段。

**Request Body**

```json
{
  "nickname": "新昵称",
  "avatar_url": "https://example.com/new-avatar.jpg"
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| nickname | string | ❌ | 昵称，最长 100 字符 |
| avatar_url | string | ❌ | 头像地址，最长 500 字符 |

**Response 200**：同 2.1

---

## 三、家庭模块

### 3.1 创建家庭

**POST** `/api/homes`

需要 Token。创建者自动成为 Owner。

**Request Body**

```json
{
  "name": "老王家",
  "slogan": "欢迎来到老王家，吃好喝好！",
  "cover_image": "https://example.com/cover.jpg",
  "theme": "default"
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | ✅ | 家的名称，最长 100 字符 |
| slogan | string | ❌ | 口号，最长 255 字符 |
| cover_image | string | ❌ | 封面图地址，最长 500 字符 |
| theme | string | ❌ | 主题，默认 "default" |

**Response 200**

```json
{
  "id": 1,
  "name": "老王家",
  "slogan": "欢迎来到老王家，吃好喝好！",
  "cover_image": "https://example.com/cover.jpg",
  "theme": "default",
  "owner_id": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

---

### 3.2 获取家庭信息

**GET** `/api/homes/{home_id}`

无需 Token。

**Path 参数**

| 参数 | 说明 |
|---|---|
| home_id | 家庭 ID |

**Response 200**：同 3.1 响应格式

---

### 3.3 更新家庭信息

**POST** `/api/homes/{home_id}/update`

需要 Token，且必须是该家庭的 Owner。

**Path 参数**

| 参数 | 说明 |
|---|---|
| home_id | 家庭 ID |

**Request Body**（字段均可选）

```json
{
  "name": "新名字",
  "slogan": "新口号",
  "cover_image": "https://example.com/new-cover.jpg",
  "theme": "warm"
}
```

**Response 200**：同 3.1 响应格式

---

## 四、大厨模块

### 4.1 获取大厨列表

**GET** `/api/homes/{home_id}/chefs`

无需 Token。

**Path 参数**

| 参数 | 说明 |
|---|---|
| home_id | 家庭 ID |

**Response 200**

```json
[
  {
    "id": 1,
    "home_id": 1,
    "name": "王大厨",
    "avatar_url": "https://example.com/chef.jpg",
    "is_friend": false,
    "bio": "做饭 20 年，拿手菜红烧肉",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

| 字段 | 类型 | 说明 |
|---|---|---|
| id | number | 大厨 ID |
| home_id | number | 所属家庭 ID |
| name | string | 大厨名字 |
| avatar_url | string | 头像地址 |
| is_friend | boolean | 是否"朋友出品" |
| bio | string\|null | 简介 |

---

### 4.2 添加大厨

**POST** `/api/homes/{home_id}/chefs`

需要 Token，且必须是 Owner。

**Request Body**

```json
{
  "name": "李阿姨",
  "avatar_url": "https://example.com/chef2.jpg",
  "is_friend": true,
  "bio": "邻居家阿姨，擅长粤菜"
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | ✅ | 大厨名字，最长 100 字符 |
| avatar_url | string | ✅ | 头像地址，最长 500 字符 |
| is_friend | boolean | ❌ | 是否朋友出品，默认 false |
| bio | string | ❌ | 简介，最长 500 字符 |

**Response 200**：同 4.1 单条格式

---

### 4.3 更新大厨信息

**POST** `/api/chefs/{chef_id}/update`

需要 Token，且必须是 Owner。

**Path 参数**

| 参数 | 说明 |
|---|---|
| chef_id | 大厨 ID |

**Request Body**（字段均可选）

```json
{
  "name": "新名字",
  "avatar_url": "https://example.com/new.jpg",
  "is_friend": true,
  "bio": "新简介"
}
```

**Response 200**：同 4.1 单条格式

---

### 4.4 删除大厨

**POST** `/api/chefs/{chef_id}/delete`

需要 Token，且必须是 Owner。

**Path 参数**

| 参数 | 说明 |
|---|---|
| chef_id | 大厨 ID |

**Response 200**

```json
{
  "message": "Chef deleted successfully"
}
```

---

## 五、菜品模块

### 5.1 获取菜品列表

**GET** `/api/homes/{home_id}/dishes`

无需 Token，支持分类筛选和分页。

**Path 参数**

| 参数 | 说明 |
|---|---|
| home_id | 家庭 ID |

**Query 参数**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| category | string | ❌ | - | 分类筛选：冷菜/热菜/汤/甜点/饮品/咖啡 |
| page | number | ❌ | 1 | 页码，从 1 开始 |
| page_size | number | ❌ | 20 | 每页条数，最大 100 |

**示例**: `GET /api/homes/1/dishes?category=热菜&page=1&page_size=10`

**Response 200**

```json
{
  "items": [
    {
      "id": 1,
      "home_id": 1,
      "name": "红烧肉",
      "description": "肥而不腻，入口即化",
      "category": "热菜",
      "chef_id": 1,
      "avg_rating": "4.80",
      "review_count": 5,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "images": [
        {
          "id": 1,
          "url": "https://example.com/dish1.jpg",
          "sort_order": 0
        }
      ]
    }
  ],
  "total": 20,
  "page": 1,
  "page_size": 10
}
```

---

### 5.2 创建菜品

**POST** `/api/homes/{home_id}/dishes`

需要 Token，且必须是 Owner。

**Request Body**

```json
{
  "name": "红烧肉",
  "description": "肥而不腻，入口即化",
  "category": "热菜",
  "chef_id": 1,
  "image_urls": [
    "https://example.com/dish1.jpg",
    "https://example.com/dish2.jpg"
  ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | ✅ | 菜品名称，最长 100 字符 |
| description | string | ❌ | 描述 |
| category | string | ✅ | 分类：冷菜/热菜/汤/甜点/饮品/咖啡 |
| chef_id | number | ✅ | 大厨 ID |
| image_urls | string[] | ❌ | 图片地址列表，按顺序排列 |

**Response 200**：同 5.1 items 单条格式

---

### 5.3 获取菜品详情

**GET** `/api/dishes/{dish_id}`

无需 Token。返回菜品信息及所有图片。

**Path 参数**

| 参数 | 说明 |
|---|---|
| dish_id | 菜品 ID |

**Response 200**：同 5.1 items 单条格式

---

### 5.4 更新菜品

**POST** `/api/dishes/{dish_id}/update`

需要 Token，且必须是 Owner。

**Path 参数**

| 参数 | 说明 |
|---|---|
| dish_id | 菜品 ID |

**Request Body**（字段均可选）

```json
{
  "name": "新菜名",
  "description": "新描述",
  "category": "冷菜",
  "chef_id": 2,
  "image_urls": ["https://example.com/new.jpg"]
}
```

> ⚠️ `image_urls` 若传入，会**全量替换**原有图片列表；若不传则不变。

**Response 200**：同 5.1 items 单条格式

---

### 5.5 删除菜品

**POST** `/api/dishes/{dish_id}/delete`

需要 Token，且必须是 Owner。

**Path 参数**

| 参数 | 说明 |
|---|---|
| dish_id | 菜品 ID |

**Response 200**

```json
{
  "message": "Dish deleted successfully"
}
```

---

## 六、评价模块

### 6.1 获取评价列表

**GET** `/api/dishes/{dish_id}/reviews`

无需 Token，支持分页。

**Path 参数**

| 参数 | 说明 |
|---|---|
| dish_id | 菜品 ID |

**Query 参数**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| page | number | ❌ | 1 | 页码 |
| page_size | number | ❌ | 20 | 每页条数，最大 100 |

**Response 200**

```json
{
  "items": [
    {
      "id": 1,
      "dish_id": 1,
      "user_id": 2,
      "rating": 5,
      "content": "太好吃了！！！",
      "like_count": 3,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "user_nickname": "李四",
      "user_avatar_url": "https://example.com/user2.jpg"
    }
  ],
  "total": 5,
  "page": 1,
  "page_size": 20
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| rating | number | 星级，1-5 |
| content | string\|null | 评价文字 |
| like_count | number | 点赞数 |
| user_nickname | string\|null | 评价者昵称 |
| user_avatar_url | string\|null | 评价者头像 |

---

### 6.2 发表评价

**POST** `/api/dishes/{dish_id}/reviews`

需要 Token。发表后会自动更新菜品的 `avg_rating` 和 `review_count`。

**Request Body**

```json
{
  "rating": 5,
  "content": "太好吃了，下次还来！"
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| rating | number | ✅ | 星级，1-5 整数 |
| content | string | ❌ | 评价文字 |

**Response 200**：同 6.1 items 单条格式

---

### 6.3 点赞评价

**POST** `/api/reviews/{review_id}/like`

无需 Token。每次调用点赞数 +1。

**Path 参数**

| 参数 | 说明 |
|---|---|
| review_id | 评价 ID |

**Response 200**

```json
{
  "message": "Review liked",
  "like_count": 4
}
```

---

## 附录：数据字典

### 菜品分类（category）

| 值 | 说明 |
|---|---|
| 冷菜 | 冷盘、凉菜 |
| 热菜 | 炒菜、炖菜等 |
| 汤 | 汤品 |
| 甜点 | 甜品、点心 |
| 饮品 | 饮料、果汁 |
| 咖啡 | 咖啡类 |

### 主题（theme）

| 值 | 说明 |
|---|---|
| default | 默认主题 |
| warm | 温暖橙色系 |
| modern | 现代简约 |

---

## 附录：接口总览

| 模块 | 方法 | 路径 | 需要登录 | 需要 Owner |
|---|---|---|---|---|
| 认证 | POST | /api/auth/wx-login | ❌ | ❌ |
| 用户 | GET | /api/users/me | ✅ | ❌ |
| 用户 | POST | /api/users/me/update | ✅ | ❌ |
| 家庭 | POST | /api/homes | ✅ | ❌ |
| 家庭 | GET | /api/homes/{home_id} | ❌ | ❌ |
| 家庭 | POST | /api/homes/{home_id}/update | ✅ | ✅ |
| 大厨 | GET | /api/homes/{home_id}/chefs | ❌ | ❌ |
| 大厨 | POST | /api/homes/{home_id}/chefs | ✅ | ✅ |
| 大厨 | POST | /api/chefs/{chef_id}/update | ✅ | ✅ |
| 大厨 | POST | /api/chefs/{chef_id}/delete | ✅ | ✅ |
| 菜品 | GET | /api/homes/{home_id}/dishes | ❌ | ❌ |
| 菜品 | POST | /api/homes/{home_id}/dishes | ✅ | ✅ |
| 菜品 | GET | /api/dishes/{dish_id} | ❌ | ❌ |
| 菜品 | POST | /api/dishes/{dish_id}/update | ✅ | ✅ |
| 菜品 | POST | /api/dishes/{dish_id}/delete | ✅ | ✅ |
| 评价 | GET | /api/dishes/{dish_id}/reviews | ❌ | ❌ |
| 评价 | POST | /api/dishes/{dish_id}/reviews | ✅ | ❌ |
| 评价 | POST | /api/reviews/{review_id}/like | ❌ | ❌ |
