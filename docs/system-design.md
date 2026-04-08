# 系统分析与设计文档

## 1. 系统概述

本系统由三个应用协同工作，实现从 PDF 模版解析到浏览器表单自动填充的完整闭环。

```
┌─────────────────────┐     HTTP/API      ┌──────────────────────────┐
│   百炼智能体         │ ───────────────►   │   后端服务 (FastAPI)       │
│  (PDF 解析)         │  POST /pdf-records │   数据中转 + 持久化         │
└─────────────────────┘                   └────────────┬─────────────┘
                                                       │  MySQL
                                                       │  GET /pdf-records
                                                       ▼
                                          ┌──────────────────────────┐
                                          │      浏览器插件           │
                                          │   识别表单 + 自动填充     │
                                          └──────────────────────────┘
```

---

## 2. 各应用职责

### 2.1 百炼智能体（阿里云百炼平台）

- 接收上传的模版 PDF 文件
- 调用大模型能力解析 PDF 结构，提取字段信息，输出结构化 JSON
- 通过自定义 HTTP 接口将解析结果推送到后端服务

**输出数据示例：**
```json
{
  "file_name": "入职申请表.pdf",
  "parse_result": {
    "姓名": "",
    "身份证号": "",
    "入职日期": "",
    "部门": ""
  }
}
```

---

### 2.2 后端服务（Python FastAPI）

数据中转与持久化核心，同时服务于智能体和浏览器插件。

**技术栈：**
- FastAPI + SQLAlchemy (async)
- MySQL 8.0
- Docker 容器化部署

**现有接口：**

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/pdf-records` | 百炼智能体推送解析结果 |
| GET  | `/api/pdf-records` | 浏览器插件拉取记录列表（支持分页、文件名模糊查询） |
| GET  | `/api/pdf-records/{id}` | 浏览器插件拉取单条记录详情 |

**数据模型：**

```sql
CREATE TABLE pdf_records (
  id          BIGINT       PRIMARY KEY AUTO_INCREMENT,
  file_name   VARCHAR(255) NOT NULL COMMENT 'PDF文件名',
  parse_result JSON        NOT NULL COMMENT '解析结果JSON',
  created_at  DATETIME     NOT NULL,
  updated_at  DATETIME     NOT NULL
);
```

---

### 2.3 浏览器插件

负责在目标网页上获取 PDF 解析数据并填充表单，有两种实现方案。

---

#### 方案一：Popup 弹窗，用户手动选择数据（推荐）

**工作流程：**
```
用户点击插件图标
  └─► 弹出 Popup 面板
        └─► 请求 GET /api/pdf-records 展示记录列表
              └─► 用户选择某条记录
                    └─► 插件将 parse_result 填入当前页面表单
```

**优点：**
- 用户主动触发，填充结果可预期，不会误填
- 无需识别表单类型，兼容任意页面结构
- 实现简单，稳定性高
- 用户可以在填充前预览数据内容，确认无误再操作

**缺点：**
- 需要用户手动操作，自动化程度低
- 字段映射仍需一定规则（parse_result 的 key 如何对应表单 input）

---

#### 方案二：自动识别表单类型并填充

**工作流程：**
```
页面加载
  └─► 插件扫描页面所有 input/select/textarea
        └─► 分析字段 name/id/placeholder/label 等属性
              └─► 与 parse_result 的 key 做匹配
                    └─► 自动填入匹配到的字段
```

**优点：**
- 全自动，用户无感知，体验流畅
- 适合表单结构固定、字段命名规范的场景

**缺点：**
- 表单类型多样，字段命名不统一（如"姓名"/"name"/"xingming"），匹配准确率难以保证
- `parse_result` 数据量大时，字段映射逻辑复杂，容易错填
- 不同网站 DOM 结构差异大，维护成本高
- 自动填充可能触发页面的校验逻辑或事件监听，导致异常

---

#### 方案对比

| 维度 | 方案一（Popup 手动） | 方案二（自动识别） |
|------|------|------|
| 实现难度 | 低 | 高 |
| 填充准确率 | 高（用户确认） | 不稳定（依赖字段匹配） |
| 用户操作成本 | 需点击选择 | 无需操作 |
| 兼容性 | 强（与页面结构无关） | 弱（强依赖页面 DOM） |
| 适用场景 | 表单类型多、数据复杂 | 表单固定、字段规范 |

#### 建议

优先实现**方案一**作为基础版本，保证稳定可用。后续若目标表单结构固定，可在方案一基础上叠加自动匹配逻辑作为辅助填充，用户仍可在 Popup 中确认和修正。

---

## 3. 数据流转图

```
PDF 文件
  │
  ▼
百炼智能体解析
  │  POST /api/pdf-records
  │  { file_name, parse_result }
  ▼
FastAPI 后端
  │  写入 MySQL
  ▼
MySQL 数据库
  │
  │  GET /api/pdf-records
  ▼
浏览器插件
  │
  ▼
自动填充网页表单
```

---

## 4. 部署方案

### 4.1 目标机器环境要求与安装步骤

目标机器只需安装 **Docker** 和 **Docker Compose**，其余依赖全部在容器内运行，不污染宿主机。

#### 支持的操作系统
- macOS 10.15+
- Windows 10/11（需开启 WSL2）
- Linux（Ubuntu 20.04+ / CentOS 7+）

---

#### macOS

```bash
# 1. 下载并安装 Docker Desktop（含 Docker Compose）
# https://www.docker.com/products/docker-desktop/
# 安装完成后启动 Docker Desktop

# 2. 验证安装
docker --version
docker compose version
```

---

#### Windows

```powershell
# 1. 开启 WSL2（管理员 PowerShell 执行）
wsl --install

# 2. 下载并安装 Docker Desktop
# https://www.docker.com/products/docker-desktop/
# 安装时勾选 "Use WSL 2 instead of Hyper-V"

# 3. 验证安装
docker --version
docker compose version
```

---

#### Linux（Ubuntu）

```bash
# 1. 卸载旧版本（如有）
sudo apt remove docker docker-engine docker.io containerd runc

# 2. 安装依赖
sudo apt update
sudo apt install -y ca-certificates curl gnupg

# 3. 添加 Docker 官方 GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 4. 添加 Docker 软件源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. 安装 Docker Engine + Docker Compose
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 6. 将当前用户加入 docker 组（避免每次 sudo）
sudo usermod -aG docker $USER
newgrp docker

# 7. 验证安装
docker --version
docker compose version
```

---

#### 浏览器要求

浏览器插件目前支持 Chrome / Edge（Chromium 内核），确保版本在以下范围：
- Chrome 88+
- Edge 88+

---

### 4.2 目标环境说明

部署在他人本地机器，要求：
- 环境隔离，不污染宿主机
- 一键启动，无需手动配置环境
- 数据持久化，重启不丢失

### 4.3 Docker Compose 部署（推荐）

**目录结构：**
```
deploy/
├── docker-compose.yml
├── .env                  # 环境变量配置（不提交 git）
└── .env.example          # 示例配置（提交 git）
```

**docker-compose.yml：**
```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    container_name: pdf_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    command: --default-authentication-plugin=mysql_native_password
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    image: my-fastapi-project:latest   # 本地 build 或从镜像仓库拉取
    container_name: pdf_api
    restart: always
    ports:
      - "8000:8000"
    environment:
      FASTAPI_DATABASE_URL: mysql+aiomysql://${MYSQL_USER}:${MYSQL_ROOT_PASSWORD}@db:3306/${MYSQL_DATABASE}
      FASTAPI_DEBUG: "false"
    depends_on:
      db:
        condition: service_healthy

volumes:
  mysql_data:
```

**.env.example：**
```
MYSQL_ROOT_PASSWORD=changeme
MYSQL_DATABASE=pdf_records_db
MYSQL_USER=root
```

**启动命令：**
```bash
# 1. 复制配置
cp .env.example .env
# 编辑 .env 修改密码

# 2. 构建镜像（首次或代码更新后）
docker build -t my-fastapi-project:latest .

# 3. 启动所有服务
docker compose up -d

# 4. 查看日志
docker compose logs -f api
```

### 4.4 浏览器插件部署

浏览器插件无需服务器，直接在目标机器的浏览器中加载：

1. 打开 Chrome → `chrome://extensions/`
2. 开启「开发者模式」
3. 点击「加载已解压的扩展程序」，选择插件目录
4. 插件中配置后端服务地址：`http://localhost:8000`

### 4.5 百炼智能体配置

百炼智能体服务与后端服务部署在同一台本地机器上，直接使用 `localhost` 访问即可。

在百炼智能体的自定义插件/工作流中，配置回调地址：
```
POST http://localhost:8000/api/pdf-records
```

> 注意：若百炼智能体运行在 Docker 容器内，容器中的 `localhost` 指向容器自身而非宿主机，需改用宿主机 IP（如 `http://host.docker.internal:8000/api/pdf-records`，适用于 Mac/Windows）或 `http://172.17.0.1:8000`（Linux）。
