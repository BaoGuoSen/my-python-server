# SQL 示例数据

各表 INSERT 语句示例，按外键依赖顺序执行。

---

## 执行顺序

`user` → `home` → `chef` → `dish` → `dish_image` → `review`

---

## 1. user（用户表）

```sql
INSERT INTO user (open_id, nickname, avatar_url, created_at, updated_at)
VALUES
  ('o_wx_test_001', '张小厨', 'https://example.com/avatars/user1.jpg', NOW(), NOW()),
  ('o_wx_test_002', '李美食', 'https://example.com/avatars/user2.jpg', NOW(), NOW()),
  ('o_wx_test_003', '王大厨', 'https://example.com/avatars/user3.jpg', NOW(), NOW());
```

> `id` 自增，`open_id` 是微信小程序 openid，全局唯一。

---

## 2. home（家庭厨房表）

```sql
-- 依赖：user.id（owner_id）
INSERT INTO home (name, slogan, cover_image, theme, owner_id, created_at, updated_at)
VALUES
  ('张家小厨', '家的味道，妈妈的爱', 'https://example.com/covers/home1.jpg', 'warm', 1, NOW(), NOW()),
  ('李家饭堂', '每天都有新菜式', 'https://example.com/covers/home2.jpg', 'default', 2, NOW(), NOW()),
  ('王氏私厨', '传承百年家味', 'https://example.com/covers/home3.jpg', 'classic', 3, NOW(), NOW());
```

> `owner_id` 关联 `user.id`，先确认 user 存在再插入。

---

## 3. chef（厨师表）

```sql
-- 依赖：home.id（home_id）
INSERT INTO chef (home_id, name, avatar_url, is_friend, bio, created_at, updated_at)
VALUES
  (1, '妈妈', 'https://example.com/avatars/chef1.jpg', FALSE, '做了30年家常菜，擅长川菜', NOW(), NOW()),
  (1, '爸爸', 'https://example.com/avatars/chef2.jpg', FALSE, '周末烧烤达人', NOW(), NOW()),
  (1, '王大厨（朋友）', 'https://example.com/avatars/chef3.jpg', TRUE, '米其林餐厅前主厨', NOW(), NOW()),
  (2, '李妈妈', 'https://example.com/avatars/chef4.jpg', FALSE, '粤菜家常料理专家', NOW(), NOW()),
  (3, '王爷爷', 'https://example.com/avatars/chef5.jpg', FALSE, '传统鲁菜手艺人', NOW(), NOW());
```

> `is_friend = TRUE` 表示该厨师是家庭以外的朋友厨师。

---

## 4. dish（菜品表）

```sql
-- 依赖：home.id（home_id）、chef.id（chef_id）
INSERT INTO dish (home_id, name, description, category, chef_id, avg_rating, review_count, created_at, updated_at)
VALUES
  (1, '红烧肉', '软糯香甜，入口即化，妈妈的拿手好菜', '荤菜', 1, 0.00, 0, NOW(), NOW()),
  (1, '麻婆豆腐', '麻辣鲜香，豆腐嫩滑，下饭神器', '荤菜', 1, 0.00, 0, NOW(), NOW()),
  (1, '烤羊排', '外焦里嫩，香气扑鼻', '烧烤', 2, 0.00, 0, NOW(), NOW()),
  (1, '法式鹅肝', '高端食材，精致料理', '西餐', 3, 0.00, 0, NOW(), NOW()),
  (2, '清蒸鲈鱼', '鱼肉鲜嫩，蒸出原汁原味', '海鲜', 4, 0.00, 0, NOW(), NOW()),
  (2, '白切鸡', '皮滑肉嫩，配上姜葱油', '荤菜', 4, 0.00, 0, NOW(), NOW()),
  (3, '糖醋里脊', '酸甜可口，外酥里嫩', '荤菜', 5, 0.00, 0, NOW(), NOW()),
  (3, '葱烧海参', '传统鲁菜经典，浓汁裹海参', '海鲜', 5, 0.00, 0, NOW(), NOW());
```

> `avg_rating` 和 `review_count` 建议初始为 `0.00` 和 `0`，由业务逻辑更新。
> `category` 建议统一枚举值，如：荤菜、素菜、汤品、海鲜、主食、烧烤、西餐、甜点。

---

## 5. dish_image（菜品图片表）

```sql
-- 依赖：dish.id（dish_id）
INSERT INTO dish_image (dish_id, url, sort_order, created_at)
VALUES
  (1, 'https://home-cook-source-1305243549.cos.ap-chengdu.myqcloud.com/images/hongshaorou_1.jpg', 0, NOW()),
  (1, 'https://home-cook-source-1305243549.cos.ap-chengdu.myqcloud.com/images/hongshaorou_2.jpg', 1, NOW()),
  (2, 'https://home-cook-source-1305243549.cos.ap-chengdu.myqcloud.com/images/mapodoufu_1.jpg', 0, NOW()),
  (3, 'https://home-cook-source-1305243549.cos.ap-chengdu.myqcloud.com/images/kaoyangpai_1.jpg', 0, NOW()),
  (5, 'https://home-cook-source-1305243549.cos.ap-chengdu.myqcloud.com/images/qingzhenglv_1.jpg', 0, NOW()),
  (6, 'https://home-cook-source-1305243549.cos.ap-chengdu.myqcloud.com/images/baiqieji_1.jpg', 0, NOW());
```

> `sort_order` 从 0 开始，数字越小排越前。
> 一道菜可以有多张图片。

---

## 6. review（评价表）

```sql
-- 依赖：dish.id、home.id、user.id
INSERT INTO review (dish_id, home_id, user_id, rating, content, like_count, created_at, updated_at)
VALUES
  (1, 1, 1, 5, '太好吃了！肉质软烂，甜而不腻，每次都想多吃两碗饭', 3, NOW(), NOW()),
  (1, 1, 2, 4, '味道很好，下次希望多放点糖', 1, NOW(), NOW()),
  (2, 1, 1, 5, '正宗川味，麻辣过瘾！妈妈的手艺无敌', 2, NOW(), NOW()),
  (3, 1, 2, 5, '爸爸的烤羊排每次都完美，朋友来必点', 5, NOW(), NOW()),
  (5, 2, 3, 4, '鱼很新鲜，蒸得刚好，就是葱丝可以多一些', 0, NOW(), NOW()),
  (6, 2, 1, 5, '白切鸡皮爽肉滑，姜葱油的搭配绝了', 2, NOW(), NOW()),
  (7, 3, 2, 4, '糖醋口味正宗，里脊炸得很酥', 1, NOW(), NOW()),
  (8, 3, 3, 5, '爷爷的葱烧海参真的是一绝，海参软糯入味', 4, NOW(), NOW());
```

> `rating` 范围 1-5（整数）。
> `home_id` 需要与 `dish.home_id` 一致。

---

## 完整顺序执行脚本

```sql
-- ========================================
-- 清空数据（注意外键顺序，从子表到父表）
-- ========================================
DELETE FROM review;
DELETE FROM dish_image;
DELETE FROM dish;
DELETE FROM chef;
DELETE FROM home;
DELETE FROM user;

-- ========================================
-- 插入测试数据（从父表到子表）
-- ========================================

-- 1. 用户
INSERT INTO user (open_id, nickname, avatar_url, created_at, updated_at) VALUES
  ('o_wx_test_001', '张小厨', 'https://example.com/avatars/user1.jpg', NOW(), NOW()),
  ('o_wx_test_002', '李美食', 'https://example.com/avatars/user2.jpg', NOW(), NOW()),
  ('o_wx_test_003', '王大厨', 'https://example.com/avatars/user3.jpg', NOW(), NOW());

-- 2. 家庭厨房
INSERT INTO home (name, slogan, cover_image, theme, owner_id, created_at, updated_at) VALUES
  ('张家小厨', '家的味道，妈妈的爱', 'https://example.com/covers/home1.jpg', 'warm', 1, NOW(), NOW()),
  ('李家饭堂', '每天都有新菜式', 'https://example.com/covers/home2.jpg', 'default', 2, NOW(), NOW()),
  ('王氏私厨', '传承百年家味', 'https://example.com/covers/home3.jpg', 'classic', 3, NOW(), NOW());

-- 3. 厨师
INSERT INTO chef (home_id, name, avatar_url, is_friend, bio, created_at, updated_at) VALUES
  (1, '妈妈', 'https://example.com/avatars/chef1.jpg', FALSE, '做了30年家常菜，擅长川菜', NOW(), NOW()),
  (1, '爸爸', 'https://example.com/avatars/chef2.jpg', FALSE, '周末烧烤达人', NOW(), NOW()),
  (1, '王大厨（朋友）', 'https://example.com/avatars/chef3.jpg', TRUE, '米其林餐厅前主厨', NOW(), NOW()),
  (2, '李妈妈', 'https://example.com/avatars/chef4.jpg', FALSE, '粤菜家常料理专家', NOW(), NOW()),
  (3, '王爷爷', 'https://example.com/avatars/chef5.jpg', FALSE, '传统鲁菜手艺人', NOW(), NOW());

-- 4. 菜品
INSERT INTO dish (home_id, name, description, category, chef_id, avg_rating, review_count, created_at, updated_at) VALUES
  (1, '红烧肉', '软糯香甜，入口即化，妈妈的拿手好菜', '荤菜', 1, 0.00, 0, NOW(), NOW()),
  (1, '麻婆豆腐', '麻辣鲜香，豆腐嫩滑，下饭神器', '荤菜', 1, 0.00, 0, NOW(), NOW()),
  (1, '烤羊排', '外焦里嫩，香气扑鼻', '烧烤', 2, 0.00, 0, NOW(), NOW()),
  (1, '法式鹅肝', '高端食材，精致料理', '西餐', 3, 0.00, 0, NOW(), NOW()),
  (2, '清蒸鲈鱼', '鱼肉鲜嫩，蒸出原汁原味', '海鲜', 4, 0.00, 0, NOW(), NOW()),
  (2, '白切鸡', '皮滑肉嫩，配上姜葱油', '荤菜', 4, 0.00, 0, NOW(), NOW()),
  (3, '糖醋里脊', '酸甜可口，外酥里嫩', '荤菜', 5, 0.00, 0, NOW(), NOW()),
  (3, '葱烧海参', '传统鲁菜经典，浓汁裹海参', '海鲜', 5, 0.00, 0, NOW(), NOW());

-- 5. 菜品图片
INSERT INTO dish_image (dish_id, url, sort_order, created_at) VALUES
  (1, 'https://home-cook-source-1305243549.cos.ap-chengdu.myqcloud.com/images/hongshaorou_1.jpg', 0, NOW()),
  (1, 'https://home-cook-source-1305243549.cos.ap-chengdu.myqcloud.com/images/hongshaorou_2.jpg', 1, NOW()),
  (2, 'https://home-cook-source-1305243549.cos.ap-chengdu.myqcloud.com/images/mapodoufu_1.jpg', 0, NOW()),
  (3, 'https://home-cook-source-1305243549.cos.ap-chengdu.myqcloud.com/images/kaoyangpai_1.jpg', 0, NOW()),
  (5, 'https://home-cook-source-1305243549.cos.ap-chengdu.myqcloud.com/images/qingzhenglv_1.jpg', 0, NOW()),
  (6, 'https://home-cook-source-1305243549.cos.ap-chengdu.myqcloud.com/images/baiqieji_1.jpg', 0, NOW());

-- 6. 评价
INSERT INTO review (dish_id, home_id, user_id, rating, content, like_count, created_at, updated_at) VALUES
  (1, 1, 1, 5, '太好吃了！肉质软烂，甜而不腻，每次都想多吃两碗饭', 3, NOW(), NOW()),
  (1, 1, 2, 4, '味道很好，下次希望多放点糖', 1, NOW(), NOW()),
  (2, 1, 1, 5, '正宗川味，麻辣过瘾！妈妈的手艺无敌', 2, NOW(), NOW()),
  (3, 1, 2, 5, '爸爸的烤羊排每次都完美，朋友来必点', 5, NOW(), NOW()),
  (5, 2, 3, 4, '鱼很新鲜，蒸得刚好，就是葱丝可以多一些', 0, NOW(), NOW()),
  (6, 2, 1, 5, '白切鸡皮爽肉滑，姜葱油的搭配绝了', 2, NOW(), NOW()),
  (7, 3, 2, 4, '糖醋口味正宗，里脊炸得很酥', 1, NOW(), NOW()),
  (8, 3, 3, 5, '爷爷的葱烧海参真的是一绝，海参软糯入味', 4, NOW(), NOW());
```

---

## 注意事项

- **`id` 为自增主键**，不需要手动插入，数据库会自动分配
- **外键约束**：必须按 `user → home → chef → dish → dish_image → review` 顺序插入
- **清空顺序**：与插入顺序相反，从 `review` 到 `user`
- **实际环境**：`open_id` 来自微信小程序，测试时用任意唯一字符串代替
- **图片 URL**：`dish_image.url` 需替换为通过 `/api/upload/image` 接口上传后返回的真实 COS 地址
