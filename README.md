# RAGkefu — 企业级智能客服 RAG 系统

面向电商场景的混合检索智能客服：优先数据库精确查询（订单 / 物流 / 退款 / SKU），未命中再走 FAQ 向量检索，回答带来源溯源，并配套 LangSmith + Prometheus + Grafana 与 Docker Compose 部署。

## 当前状态

- 阶段：S01 仓库脚手架已就绪
- 业务代码：尚未实现（按小步骤推进）

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

## 快速启动（后续步骤补充）

```bash
# S02+ 将补充依赖安装与服务启动命令
```

## 协作约定

- 小步骤交付，一步一验证、一步一 commit
- commit message 使用约定式前缀 + 中文描述（如 `chore: 初始化仓库脚手架`）
