# CrossBorder AI Agent - 企业级优化计划

## 一、项目概述

**目标**：将现有跨境电商AI运营助手从原型级项目升级为面试级企业产品，侧重AI/LLM应用开发方向。

**核心方向**：
- 架构升级：FastAPI后端 + Streamlit前端，前后端分离
- 多模型支持：MiniMax / OpenAI / 本地模型可切换
- 工程化提升：配置管理、日志系统、异常处理、类型注解、单元测试
- 功能增强：商品描述生成、多平台支持、历史任务管理

---

## 二、当前状态分析

### 2.1 现有文件清单（不含.venv）

| 文件 | 行数 | 职责 |
|------|------|------|
| `app.py` | 25 | 命令行入口，硬编码测试数据 |
| `streamlit_app.py` | 321 | Streamlit前端，UI+业务逻辑混合 |
| `services/ai_client.py` | 56 | MiniMax API调用，仅支持单模型 |
| `services/title_generator.py` | 58 | 标题生成，硬编码prompt |
| `services/seo_generator.py` | 49 | SEO关键词生成，硬编码prompt |
| `utils/db_manager.py` | 321 | SQLite数据库CRUD，无连接池 |
| `utils/excel_exporter.py` | 60 | Excel导出 |
| `utils/history_manager.py` | 48 | JSON文件历史记录 |
| `utils/json_parser.py` | 20 | JSON解析，错误处理简陋 |
| `utils/review_manager.py` | 12 | JSON文件审核状态管理 |
| `requirements.txt` | 58 | 依赖清单（含间接依赖） |
| `.env` | 1 | API密钥（明文） |
| `README.md` | 0 | 空文件 |

### 2.2 核心问题

1. **架构问题**：前后端耦合，streamlit_app.py 承载了UI渲染+业务逻辑+数据访问
2. **安全问题**：API密钥明文存储，.env未加入.gitignore，无.gitignore文件
3. **模型耦合**：仅支持MiniMax单模型，硬编码在ai_client.py中
4. **数据层问题**：review_manager用JSON文件存储审核状态（与DB重复），db_manager无连接池/上下文管理器
5. **代码质量**：无类型注解、无日志系统、无单元测试、无__init__.py、无配置管理
6. **功能单一**：仅支持标题生成和SEO关键词，仅支持Amazon平台
7. **项目规范缺失**：无.gitignore、README为空、requirements.txt包含间接依赖

---

## 三、目标架构

```
crossborder-ai-agent/
├── backend/                      # FastAPI后端
│   ├── main.py                   # FastAPI应用入口
│   ├── config.py                 # 配置管理（Pydantic Settings）
│   ├── models/                   # 数据模型（Pydantic）
│   │   ├── __init__.py
│   │   ├── product.py            # 商品信息模型
│   │   ├── content.py            # 生成内容模型
│   │   └── task.py               # 任务模型
│   ├── routers/                  # API路由
│   │   ├── __init__.py
│   │   ├── generate.py           # 内容生成API
│   │   ├── review.py             # 审核管理API
│   │   ├── task.py               # 任务管理API
│   │   └── export.py             # 导出API
│   ├── services/                 # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── ai_provider.py        # AI模型抽象基类
│   │   ├── minimax_provider.py   # MiniMax实现
│   │   ├── openai_provider.py    # OpenAI实现
│   │   ├── ollama_provider.py    # 本地模型实现
│   │   ├── content_generator.py  # 内容生成服务（策略模式）
│   │   └── prompt_builder.py     # Prompt模板管理
│   ├── db/                       # 数据访问层
│   │   ├── __init__.py
│   │   ├── database.py           # 数据库连接管理
│   │   ├── crud.py               # CRUD操作
│   │   └── migrations/           # 数据库迁移
│   │       └── init.sql
│   └── utils/                    # 工具函数
│       ├── __init__.py
│       ├── logger.py             # 日志配置
│       └── exceptions.py         # 自定义异常
├── frontend/                     # Streamlit前端
│   ├── app.py                    # Streamlit主入口
│   ├── pages/                    # 多页面
│   │   ├── 1_generate.py         # 内容生成页
│   │   ├── 2_review.py           # 内容审核页
│   │   ├── 3_history.py          # 历史记录页
│   │   └── 4_settings.py         # 设置页
│   ├── components/               # 可复用组件
│   │   ├── sidebar.py            # 侧边栏
│   │   ├── stat_cards.py         # 统计卡片
│   │   └── content_table.py      # 内容表格
│   └── api_client.py             # 后端API客户端
├── tests/                        # 测试
│   ├── __init__.py
│   ├── conftest.py               # 测试配置和fixtures
│   ├── test_ai_provider.py
│   ├── test_content_generator.py
│   ├── test_crud.py
│   └── test_api.py
├── prompts/                      # Prompt模板
│   ├── title_amazon.txt
│   ├── title_ebay.txt
│   ├── seo_amazon.txt
│   └── description_amazon.txt
├── .env.example                  # 环境变量模板
├── .gitignore
├── requirements.txt              # 仅直接依赖
├── README.md
└── Dockerfile
```

---

## 四、实施步骤

### Phase 1：项目基础设施（优先级：高）

#### 1.1 创建.gitignore
- 排除 `.venv/`、`data/`、`outputs/`、`__pycache__/`、`.env`、`*.pyc`

#### 1.2 创建.env.example
- 列出所有需要的环境变量，不包含真实密钥
- `MINIMAX_API_KEY=`、`OPENAI_API_KEY=`、`OLLAMA_BASE_URL=`、`AI_PROVIDER=minimax`

#### 1.3 创建config.py（Pydantic Settings）
- 使用 `pydantic-settings` 管理所有配置
- 支持环境变量和.env文件
- 配置项：AI_PROVIDER、各模型API_KEY、DB_PATH、LOG_LEVEL等

#### 1.4 创建logger.py
- 使用Python标准logging模块
- 支持控制台+文件双输出
- 按模块区分日志级别
- 结构化日志格式

#### 1.5 创建exceptions.py
- 自定义异常层级：`AppException` > `AIProviderException` / `DatabaseException` / `ExportException`
- 包含错误码和用户友好消息

#### 1.6 精简requirements.txt
- 仅保留直接依赖：fastapi, uvicorn, streamlit, openai, requests, python-dotenv, openpyxl, pydantic, pydantic-settings, httpx

---

### Phase 2：FastAPI后端核心（优先级：高）

#### 2.1 数据模型（Pydantic）
- `ProductInfo`：name, feature, region, platform（新增）
- `GeneratedContent`：item_id, batch_id, type(title/seo/description), content, status, created_at
- `Task`：batch_id, product_info, items, excel_path, created_at
- `ReviewAction`：item_id, action(approve/reject/restore)
- `GenerateRequest`/`GenerateResponse`：API请求响应模型

#### 2.2 AI模型抽象层（策略模式）
- `AIProvider` 抽象基类：`generate(prompt) -> str`
- `MiniMaxProvider`：现有逻辑迁移
- `OpenAIProvider`：使用openai SDK
- `OllamaProvider`：使用httpx调用本地Ollama API
- 工厂函数 `get_provider(provider_name) -> AIProvider`

#### 2.3 Prompt模板管理
- 将硬编码prompt提取到 `prompts/` 目录下的文本文件
- `PromptBuilder` 类：加载模板、填充变量、支持多平台
- 新增平台：Amazon / eBay / Shopify
- 新增内容类型：商品描述（description）

#### 2.4 内容生成服务
- `ContentGenerator` 类：编排AI调用、结果解析、重试逻辑
- 支持异步生成（asyncio）
- 支持流式响应（SSE）

#### 2.5 数据库层重构
- 使用上下文管理器管理连接（`with get_db() as conn`）
- 合并review_manager到数据库（删除JSON文件存储）
- 统一CRUD接口
- 添加索引优化查询

#### 2.6 API路由
- `POST /api/generate`：生成内容（支持标题/SEO/描述）
- `GET /api/tasks`：获取任务列表
- `GET /api/tasks/{batch_id}/items`：获取任务内容
- `PUT /api/items/{item_id}/status`：更新审核状态
- `POST /api/items/batch-review`：批量审核
- `GET /api/stats`：获取统计数据
- `GET /api/export/{batch_id}`：下载Excel

#### 2.7 FastAPI应用入口
- CORS中间件配置
- 生命周期管理（启动/关闭）
- 路由注册
- 全局异常处理

---

### Phase 3：Streamlit前端重构（优先级：高）

#### 3.1 API客户端
- 封装所有后端API调用
- 统一错误处理和重试
- 支持异步请求

#### 3.2 多页面架构
- **生成页**：商品信息输入 + 模型/平台选择 + 生成结果展示
- **审核页**：筛选 + 批量操作 + 状态切换
- **历史页**：任务列表 + 搜索 + 详情查看
- **设置页**：AI模型配置 + API密钥管理

#### 3.3 可复用组件
- `stat_cards`：统计卡片组件
- `content_table`：内容审核表格组件
- `sidebar`：导航侧边栏

---

### Phase 4：功能增强（优先级：中）

#### 4.1 商品描述生成
- 新增AI生成商品详细描述功能
- 支持不同平台格式（Amazon五点描述、eBay Item Specifics）

#### 4.2 多平台支持
- Amazon / eBay / Shopify 三平台
- 每个平台有独立的prompt模板和内容格式

#### 4.3 历史任务管理
- 任务列表展示（分页）
- 按商品名/日期搜索
- 查看历史任务详情
- 重新生成内容

#### 4.4 内容对比
- 同一商品多次生成结果对比
- 不同模型生成结果对比

---

### Phase 5：测试与文档（优先级：中）

#### 5.1 单元测试
- AI Provider测试（mock API响应）
- Content Generator测试
- CRUD操作测试
- API端点测试

#### 5.2 集成测试
- 端到端生成流程测试
- 审核工作流测试

#### 5.3 README.md
- 项目介绍、架构图、技术栈
- 安装部署指南
- API文档链接
- 项目亮点（面试重点）

#### 5.4 Dockerfile
- 多阶段构建
- 前后端分离部署

---

## 五、面试亮点设计

| 亮点 | 体现能力 | 对应实现 |
|------|---------|---------|
| 策略模式多模型切换 | 设计模式 | AIProvider抽象 + 工厂函数 |
| 前后端分离架构 | 系统设计 | FastAPI + Streamlit |
| Prompt模板引擎 | Prompt工程 | 外部化模板 + 变量填充 |
| Pydantic数据校验 | 数据工程 | 请求/响应模型 |
| 异常处理体系 | 工程规范 | 自定义异常 + 全局处理 |
| 配置管理 | 工程规范 | Pydantic Settings |
| 日志系统 | 可观测性 | 结构化日志 |
| 单元测试 | 质量保障 | pytest + mock |
| 多平台扩展 | 产品思维 | 平台抽象 |

---

## 六、实施优先级

1. **Phase 1**（基础设施）：1-2小时 → 立即可做
2. **Phase 2**（后端核心）：3-4小时 → 核心价值
3. **Phase 3**（前端重构）：2-3小时 → 用户体验
4. **Phase 4**（功能增强）：2-3小时 → 差异化
5. **Phase 5**（测试文档）：1-2小时 → 完整性

---

## 七、验证步骤

1. `pip install -r requirements.txt` 安装依赖无报错
2. `uvicorn backend.main:app --reload` 后端启动正常
3. `streamlit run frontend/app.py` 前端启动正常
4. 前端调用后端API生成内容成功
5. 切换AI模型（MiniMax/OpenAI/Ollama）均正常
6. 审核工作流（通过/拒绝/恢复）正常
7. Excel导出和下载正常
8. `pytest tests/` 全部通过
9. 无API密钥泄露到代码仓库
