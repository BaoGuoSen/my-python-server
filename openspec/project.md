# 项目上下文

## 项目目的
基于 [fastapi-mvc](https://github.com/fastapi-mvc/fastapi-mvc) 生成的 FastAPI Web 应用，提供 REST API 接口。作为构建生产级 API 的基础，包含健康检查、结构化路由和 OpenAPI 文档。

## 技术栈
- **运行时**：Python 3.8、3.9、3.10、3.11
- **框架**：FastAPI ~0.98.0
- **ASGI 服务器**：Uvicorn（开发）、Gunicorn（生产）
- **配置与校验**：Pydantic BaseSettings
- **CLI**：Click
- **包管理**：Poetry
- **测试**：pytest、pytest-cov、pytest-asyncio、httpx
- **代码检查与格式化**：Black、flake8（PEP 8、PEP 257、pyflakes）、mypy
- **文档**：Sphinx、myst-parser
- **容器化**：Docker（多阶段构建，distroless 最终镜像）

## 项目规范

### 代码风格
- **格式化工具**：Black（行宽 88 字符）
- **代码检查**：flake8，包含 PEP 8（E,W,I）、PEP 257（D）、pyflakes（F）、复杂度（C901）、TODO（T）
- **导入顺序**：通过 flake8-import-order 使用 pep8 风格
- **类型检查**：mypy 严格模式（检查未标注类型、禁止隐式 Optional 等）
- **文档字符串**：必须编写；flake8-docstrings 强制 PEP 257（忽略 D301）

### 架构模式
- **类 MVC 结构**：`app/controllers/`（路由处理）、`app/views/`（Pydantic 响应模型）、`app/models/`（领域模型）
- **路由**：根 APIRouter 使用 `/api` 前缀；控制器注册子路由并打标签
- **配置**：`config/application.py` — 使用 Pydantic `BaseSettings`，环境变量前缀为 `FASTAPI_`
- **异常**：自定义 `HTTPException` 位于 `app/exceptions/`，并有全局异常处理器
- **入口**：`my-fastapi-project serve`（CLI）、`my_fastapi_project.app:get_application`（ASGI）

### 测试策略
- **单元测试**：`tests/unit/` — 模拟依赖，隔离测试各组件
- **集成测试**：`tests/integration/` — 使用 FastAPI `TestClient`，完整请求/响应
- **覆盖率**：最低 90%（`--cov-fail-under=90`）；排除 `gunicorn.py`、`__main__.py`
- **命令**：`make unit-test`、`make integration-test`、`make test`、`make coverage`

### Git 工作流
- 未定义正式分支策略，建议采用常见实践（如 feature 分支、main/develop）。
- 仓库地址占位符：`https://your.repo.url.here`

## 领域上下文
通用 REST API 脚手架。当前能力：`/api/ready` 健康检查，返回 `{"status": "ok"}`。Redis 支持已预留但默认关闭（`USE_REDIS=false`）。业务逻辑可放在 `app/controllers/`、`app/views/` 和 `app/models/` 中。

## 重要约束
- 仅支持 Python 3.8–3.11
- MIT 许可证
- 生产镜像以 `nonroot` 用户运行（distroless）
- 应用默认绑定 `0.0.0.0:8000`

## 外部依赖
- 当前无外部依赖。Redis 为可选，默认关闭。
- Swagger UI 在 `/` 提供（可通过 `FASTAPI_DOCS_URL` 配置）。
