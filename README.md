# RAGkefu — 企业级智能客服 RAG 系统

面向电商场景的混合检索智能客服：优先数据库精确查询（订单 / 物流 / 退款 / SKU），未命中再走 FAQ 向量检索，回答带来源溯源，并配套 LangSmith + Prometheus + Grafana 与 Docker Compose 部署。

## 当前状态

- 阶段：S06–S08 已完成（路由组装 / 统一错误 / request_id 中间件）
- 下一步：Chat API 契约 mock（S09）

## 环境要求

- Python **>= 3.11**（推荐；Docker 镜像将固定版本）
- 包管理：`pip` + venv（后续可换成 uv/poetry，当前保持简单）

## 依赖文件（方案 A：分层）

| 文件 | 用途 |
|------|------|
| `requirements.txt` | 运行时基线（FastAPI / 配置 / DB / 指标） |
| `requirements-dev.txt` | 开发与测试（含基线） |
| `requirements-rag.txt` | RAG 检索栈（LangChain / Chroma / Redis 等，S22+ 再用） |

## 安装

```bash
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 日常开发（推荐）
pip install -U pip
pip install -r requirements-dev.txt

# 配置（可选；不复制则使用代码内默认值）
cp .env.example .env

# 仅运行时基线
# pip install -r requirements.txt

# 启用向量检索 / LangChain 时再装
# pip install -r requirements-rag.txt
```

## 目录结构（规划）

```text
app/                 # FastAPI 应用（api / core / schemas / services / retrieval / db）
data/                # FAQ、评测集、数据库种子数据
monitoring/          # Prometheus / Grafana 配置
deploy/              # 部署相关片段（可选）
tests/               # 单元 / 集成 / 压测
docs/                # 架构、API、运维文档
scripts/             # 种子、入库、评测脚本
```

## 快速启动

```bash
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
# 另开终端：
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/healthz
curl http://127.0.0.1:8000/v1/ping
curl "http://127.0.0.1:8000/v1/ping?q=-1"   # 统一校验错误 JSON
# API 文档：http://127.0.0.1:8000/docs
```

## 路由约定

- `/healthz`：根路径存活探针（不挂 `/v1`）
- `/v1/*`：版本化业务 API（由 `settings.api_prefix` 控制）
- 响应头 `X-Request-ID`：请求追踪；错误体含 `code/message/detail/request_id`

## 配置说明

- 模板：`.env.example`
- 加载入口：`app/core/config.py`（`get_settings()`）
- 常用变量：`APP_ENV`、`DEBUG`、`API_PREFIX`；`DATABASE_URL` / `REDIS_URL` / `CHROMA_URL` 为后续步骤预留

## 协作约定

- 小步骤交付，一步一验证、一步一 commit
- commit message 使用约定式前缀 + 中文描述（如 `chore: 初始化仓库脚手架`）
