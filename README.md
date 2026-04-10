# my-fastapi-project
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub](https://img.shields.io/badge/fastapi-v.0.98.0-blue)
![GitHub](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)
![GitHub](https://img.shields.io/badge/license-MIT-blue)

---

基于 [fastapi-mvc](https://github.com/fastapi-mvc/fastapi-mvc) 生成的 FastAPI REST API 项目，提供健康检查、结构化路由和 OpenAPI 文档，可作为生产级 API 的基础脚手架。

## 技术栈

- **框架**：FastAPI 0.98
- **运行时**：Python 3.8 / 3.9 / 3.10 / 3.11
- **ASGI 服务器**：Uvicorn（开发）、Gunicorn（生产）
- **包管理**：Poetry
- **配置与校验**：Pydantic BaseSettings

## 项目结构

```
my-fastapi-project/
├── my_fastapi_project/          # 主应用包
│   ├── app/                     # 应用逻辑
│   │   ├── controllers/         # 路由控制器（处理 HTTP 请求）
│   │   ├── views/               # Pydantic 响应模型
│   │   ├── models/              # 领域模型
│   │   ├── exceptions/          # 自定义异常及全局处理器
│   │   ├── utils/               # 工具函数
│   │   ├── router.py            # API 路由注册（/api 前缀）
│   │   └── asgi.py              # FastAPI 应用入口
│   ├── cli/                     # 命令行工具（serve 等）
│   └── config/                  # 配置（环境变量 FASTAPI_*）
├── tests/                       # 测试
│   ├── unit/                    # 单元测试
│   └── integration/             # 集成测试
├── build/                       # 构建脚本（install、image）
├── docs/                        # Sphinx 文档源码
├── openspec/                    # OpenSpec 规范与变更提案
├── pyproject.toml               # 项目依赖与配置
└── Makefile                     # 常用命令
```

## 运行方式

### 1. 安装依赖

```bash
make install
```

或使用 Poetry 直接安装：

```bash
poetry install
```

> **macOS 提示**：若遇 SSL 证书错误，可先执行 `/Applications/Python\ 3.11/Install\ Certificates.command` 或使用 `pip install poetry` 安装 Poetry。

### 2. 启动服务

```bash
my-fastapi-project serve
```

或通过 Poetry 运行：

```bash
poetry run my-fastapi-project serve
```

默认监听 `127.0.0.1:8000`。指定地址和端口：

```bash
my-fastapi-project serve --bind 0.0.0.0:8000
```

### 3. 开发模式（热重载）

```bash
poetry run uvicorn my_fastapi_project.app.asgi:get_application --factory --reload
```

### 4. Docker 运行

```bash
make image
docker run -p 8000:8000 my-fastapi-project
```

### 访问地址

- **API 健康检查**：http://127.0.0.1:8000/api/ready
- **Swagger 文档**：http://127.0.0.1:8000/swaggerUi

## 常用命令

| 命令 | 说明 |
|------|------|
| `make help` | 显示所有可用命令 |
| `make install` | 安装项目依赖 |
| `make unit-test` | 运行单元测试 |
| `make integration-test` | 运行集成测试 |
| `make test` | 运行全部测试 |
| `make coverage` | 运行测试并生成覆盖率报告（要求 ≥90%） |
| `make metrics` | 代码检查（flake8、black） |
| `make mypy` | 类型检查 |
| `make docs` | 构建文档，输出到 `./site/` |
| `make build` | 构建 Python 包 |
| `make image` | 构建 Docker 镜像 |

## 文档

手动构建文档：

```bash
make docs
```

完成后在浏览器中打开 `./site/index.html`。

## License

本项目采用 MIT 许可证。


http://guosenpower.cn/api/ready

systemctl restart home-cook

镜像信息

Ubuntu 24.04 LTS

CPU/内存

2核/2GB

系统盘

40GB SSD

带宽

3Mbps

流量包

200GB/月

公网IP地址

162.14.123.29

 vim /etc/nginx/sites-available/home-cook

 cd /app/my-python-server