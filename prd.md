# PRD：Home Cook 家庭菜单小程序

## Context

用户希望以「家庭」为单位，构建一个菜单/食谱小程序。核心场景是：有朋友来做客时，打开这个小程序，让客人或主人在真实菜品照片中选菜，并能看到历史食客的评价。每个家庭有独立的 homeId，支持数据与样式定制，体现"每个家都充满爱"的温度感。

---

## 产品定位

- **产品名**：Home Cook（家宴菜单）
- **目标用户**：有聚餐需求的家庭用户
- **核心价值**：让待客变成一种仪式感——打开小程序，像翻看餐厅菜单一样选菜，每道菜背后都有故事和评价。

---

## 核心概念

| 概念 | 说明 |
|---|---|
| Home（家） | 最小单位，通过 homeId 隔离数据与样式，每个家庭有自己的"主页" |
| 菜品（Dish） | 真实拍摄的菜，有照片、名称、描述、大厨信息 |
| 大厨（Chef） | 做这道菜的人，可以是主人也可以是朋友 |
| 食客（Guest） | 曾经吃过这道菜并留下评价的人 |
| 评价（Review） | 文字/星级评价，带食客昵称和头像，商业互吹友好 |
| 菜单（Menu） | 某次聚餐选定的菜品集合（V2） |

---

## 功能模块

### 1. 家主页（Home Page）

**入口**：扫描小程序码 → 带 homeId 参数进入

**展示内容**：
- 家的名称 + Slogan（如"欢迎来到老王家"）
- 封面图（可自定义）
- 菜品分类导航（冷菜、热菜、汤、甜点、饮品、咖啡）
- 大厨墙（展示所有大厨头像 + 名字）

**交互**：
- 点击分类 → 进入菜品列表
- 点击大厨 → 筛选该大厨的菜品

---

### 2. 菜品列表（Dish List）

**展示**：
- 瀑布流/卡片式布局
- 每张卡片：菜品照片 + 名称 + 大厨标签 + 评分

**筛选**：
- 按分类（冷菜/热菜/汤/甜点/饮品/咖啡）
- 按大厨
- 按评分排序

---

### 3. 菜品详情（Dish Detail）

**展示**：
- 多张真实照片（轮播）
- 菜名 + 描述
- 大厨信息（头像 + 名字 + 简介）
- 平均评分 + 评价数
- 评价列表（食客头像 + 昵称 + 星级 + 文字评价 + 时间）

**交互**：
- 点击"写评价" → 弹出评价表单（星级 + 文字）
- 评价提交后刷新详情页

---

### 4. 大厨管理（Owner Only）

**功能**：
- 添加大厨（名字 + 头像 + 简介）
- 标记"朋友出品"（特殊标签）
- 编辑/删除大厨

---

### 5. 菜品管理（Owner Only）

**功能**：
- 上传菜品（名称 + 描述 + 分类 + 大厨 + 多张照片）
- 编辑菜品信息
- 删除菜品

---

### 6. 评价系统

**功能**：
- 任何微信用户可对菜品打分（1-5星）+ 留言
- 评价展示在菜品详情页
- 评价可点赞（V2）

---

### 7. 用户身份

| 角色 | 权限 |
|---|---|
| Owner | 创建家、管理大厨、管理菜品 |
| Guest | 浏览菜品、写评价 |

**登录方式**：微信授权（获取 openId + 昵称 + 头像）

---

## 数据模型

### User（用户）
- id
- open_id（微信 openId）
- nickname
- avatar_url
- created_at

### Home（家）
- id
- name（家的名称）
- slogan
- cover_image
- theme（主题标识，如 default/warm/modern）
- owner_id（FK → User）
- created_at

### Chef（大厨）
- id
- home_id（FK → Home）
- name
- avatar_url
- is_friend（是否"朋友出品"）
- bio（简介）
- created_at

### Dish（菜品）
- id
- home_id（FK → Home）
- name
- description
- category（冷菜/热菜/汤/甜点/饮品/咖啡）
- chef_id（FK → Chef）
- avg_rating（平均评分，冗余字段）
- review_count（评价数，冗余字段）
- created_at

### DishImage（菜品图片）
- id
- dish_id（FK → Dish）
- url
- sort_order
- created_at

### Review（评价）
- id
- dish_id（FK → Dish）
- user_id（FK → User）
- rating（1-5）
- content
- like_count（点赞数，V2）
- created_at

---

## API 设计

### 认证
- `POST /api/auth/wx-login` — 微信登录，code 换 openId，返回 JWT

### Home
- `POST /api/homes` — 创建家（Owner）
- `GET /api/homes/{home_id}` — 获取家主页信息
- `PUT /api/homes/{home_id}` — 更新家信息（Owner）

### Chef
- `GET /api/homes/{home_id}/chefs` — 获取大厨列表
- `POST /api/homes/{home_id}/chefs` — 添加大厨（Owner）
- `PUT /api/chefs/{chef_id}` — 更新大厨（Owner）
- `DELETE /api/chefs/{chef_id}` — 删除大厨（Owner）

### Dish
- `GET /api/homes/{home_id}/dishes` — 菜品列表（支持筛选、分页）
- `POST /api/homes/{home_id}/dishes` — 创建菜品（Owner）
- `GET /api/dishes/{dish_id}` — 菜品详情
- `PUT /api/dishes/{dish_id}` — 更新菜品（Owner）
- `DELETE /api/dishes/{dish_id}` — 删除菜品（Owner）

### Review
- `GET /api/dishes/{dish_id}/reviews` — 获取评价列表
- `POST /api/dishes/{dish_id}/reviews` — 发表评价
- `POST /api/reviews/{review_id}/like` — 点赞评价（V2）

### User
- `GET /api/users/me` — 获取当前用户信息
- `PUT /api/users/me` — 更新用户信息

---

## 技术栈

- **后端**：FastAPI + SQLAlchemy + MySQL
- **前端**：微信小程序（原生）
- **存储**：阿里云 OSS（图片）
- **认证**：JWT + 微信登录

---

## MVP 范围

**必做**：
- 微信登录
- 家主页展示
- 菜品 CRUD（Owner）
- 大厨 CRUD（Owner）
- 菜品列表 + 详情
- 评价系统

**暂缓**：
- 今日菜单生成
- 主题切换 UI
- 评价点赞

---

## 验收标准

1. 扫描带 homeId 的小程序码能进入对应家主页
2. 能浏览菜品列表，点击进入详情看到真实照片和评价
3. Owner 能上传菜品并指定大厨（含朋友）
4. 食客能对菜品打分并留下评价文字
5. 不同 homeId 的数据完全隔离
