# 🤖 CrossBorder AI Agent

AI跨境电商运营助手 — 基于大语言模型的商品内容智能生成与审核平台

## ✨ 项目亮点

| 亮点 | 说明 |
|------|------|
| 🏗️ 前后端分离架构 | FastAPI后端 + Streamlit前端，RESTful API设计 |
| 🤖 多模型策略模式 | 支持MiniMax/OpenAI/Ollama，策略模式一键切换 |
| 📝 Prompt模板引擎 | 外部化Prompt管理，支持多平台模板 |
| ✅ 内容审核工作流 | 生成→审核→导出完整闭环 |
| 📊 Pydantic数据校验 | 请求/响应全链路类型安全 |
| 🗄️ MySQL数据库 | InnoDB引擎 + 索引优化 + 外键约束 + 上下文管理器 |
| 📋 结构化日志 | 按模块分级，控制台+文件双输出 |
| 🧪 单元测试覆盖 | pytest + mock，4个测试模块 |
| 🐳 容器化部署 | Dockerfile一键部署 |

## 🛠️ 技术栈

- **后端**: Python 3.11 + FastAPI + Pydantic + MySQL (PyMySQL)
- **前端**: Streamlit (多页面架构)
- **AI集成**: MiniMax / OpenAI / Ollama (策略模式)
- **数据库**: MySQL 8.0 + InnoDB + 索引优化 + 外键约束
- **数据导出**: openpyxl
- **配置管理**: pydantic-settings + .env

## 📁 项目结构

```
crossborder-ai-agent/
├── backend/                    # FastAPI后端
│   ├── main.py                 # 应用入口
│   ├── config.py               # 配置管理
│   ├── models/schemas.py       # Pydantic数据模型
│   ├── routers/                # API路由
│   │   ├── generate.py         # 内容生成API
│   │   ├── review.py           # 审核管理API
│   │   ├── task.py             # 任务管理API
│   │   └── export.py           # 导出API
│   ├── services/               # 业务逻辑
│   │   ├── ai_provider.py      # AI模型抽象层（策略模式）
│   │   ├── content_generator.py # 内容生成服务
│   │   └── prompt_builder.py   # Prompt模板管理
│   ├── db/                     # 数据访问层
│   │   ├── database.py         # 连接管理
│   │   └── crud.py             # CRUD操作
│   └── utils/                  # 工具
│       ├── logger.py           # 日志
│       ├── exceptions.py       # 异常体系
│       └── excel_exporter.py   # Excel导出
├── frontend/                   # Streamlit前端
│   ├── app.py                  # 主入口
│   ├── api_client.py           # 后端API客户端
│   ├── pages/                  # 多页面
│   │   ├── 1_generate.py       # 内容生成
│   │   ├── 2_review.py         # 内容审核
│   │   ├── 3_history.py        # 历史记录
│   │   └── 4_settings.py       # 系统设置
│   └── components/             # 可复用组件
├── prompts/                    # Prompt模板
├── tests/                      # 单元测试
├── .env.example                # 环境变量模板
├── Dockerfile                  # 容器化部署
└── requirements.txt            # 依赖清单
```

## 🚀 快速开始

### 1. 安装依赖

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入API密钥和MySQL配置
# 确保MySQL服务已启动
```

### 3. 启动服务

```bash
# 启动后端
uvicorn backend.main:app --reload

# 启动前端（新终端）
streamlit run frontend/app.py
```

### 4. Docker部署

```bash
docker build -t crossborder-ai .
docker run -p 8000:8000 -p 8501:8501 --env-file .env crossborder-ai
```

## 📡 API文档

启动后端后访问: `http://localhost:8000/docs`

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/generate` | POST | 生成内容（标题/SEO/描述） |
| `/api/tasks` | GET | 获取任务列表 |
| `/api/tasks/{batch_id}/items` | GET | 获取任务内容 |
| `/api/items/{item_id}/status` | PUT | 更新审核状态 |
| `/api/items/batch-review` | POST | 批量审核 |
| `/api/stats` | GET | 运营统计 |
| `/api/export/{batch_id}` | GET | 导出Excel |

## 🧪 运行测试

```bash
pytest tests/ -v
```

## 📌 重点

1. **策略模式**: `ai_provider.py` 中 `AIProvider` 抽象基类 + 3个实现 + 工厂函数
2. **前后端分离**: FastAPI提供RESTful API，Streamlit作为纯前端消费API
3. **Prompt工程**: 外部化模板 + 变量填充，支持多平台扩展
4. **Pydantic校验**: 请求/响应全链路数据校验，类型安全
5. **异常体系**: 自定义异常层级 + 全局异常处理中间件
6. **数据库设计**: MySQL InnoDB + 索引优化 + 外键约束 + JOIN聚合查询 + 上下文管理器
