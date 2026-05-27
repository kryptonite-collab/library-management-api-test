# 图书馆管理系统接口自动化测试项目

## 项目背景

本项目基于本地已有的图书馆管理系统课程项目，扩展了一套面向测试开发实习展示的接口自动化测试工程。测试工程统一放在 `api-tests/` 目录下，重点覆盖接口契约、异常参数、测试报告、数据库一致性校验和测试数据构造能力。

当前扩展不改动前端；后端仅围绕日志接口契约和必要的可测试性字段做了小范围调整。

## 被测系统技术栈

| 模块 | 技术 |
| --- | --- |
| 后端服务 | Node.js |
| Web 框架 | Express |
| ORM | Prisma |
| 数据库 | SQLite |

## 测试技术栈

| 能力 | 技术 |
| --- | --- |
| 测试框架 | Python + pytest |
| HTTP 请求 | requests |
| 测试报告 | Allure / allure-pytest |
| 环境配置 | python-dotenv |
| 数据库校验 | sqlite3 + SQLite |

## api-tests 目录结构

```text
api-tests/
  requirements.txt
  pytest.ini
  .env.example
  README.md
  common/
    config.py
    request_client.py
    assertions.py
    db_client.py
    data_factory.py
  scripts/
    run_tests.ps1
  tests/
    test_health.py
    test_logs_contract.py
    test_logs_params.py
    test_books_contract.py
    test_books_db_consistency.py
    test_logs_db_consistency.py
    test_books_create_flow.py
```

## RequestClient 封装

`common/request_client.py` 对 `requests` 做了统一封装：

- 统一读取 `BASE_URL` 和 `REQUEST_TIMEOUT`。
- 支持 `get/post/put/delete/request`。
- 自动拼接接口路径。
- 支持 headers、params、json body、timeout。
- 支持 `set_token()`，自动设置 `Authorization: Bearer xxx`。
- 统一返回 `status_code`、`body`、`text`、`headers`。
- 自动写入 Allure 附件，包括请求方法、URL、脱敏 headers、params、json body、响应状态码和响应 body。

Authorization 会在报告中脱敏为 `Bearer ***`，避免 token 明文泄露。

## pytest marker 分层执行

`pytest.ini` 中配置了多组 marker，用于分层执行：

| marker | 说明 |
| --- | --- |
| `smoke` | 核心冒烟测试 |
| `logs` | 系统日志接口测试 |
| `books` | 图书信息接口测试 |
| `contract` | 接口响应契约测试 |
| `negative` | 异常参数测试 |
| `db` | 数据库校验测试 |
| `consistency` | 接口与数据库一致性测试 |
| `flow` | 流程类测试或流程能力占位 |
| `regression` | 回归测试集合 |

示例：

```powershell
pytest -m smoke
pytest -m "logs and contract"
pytest -m "books and contract"
pytest -m "db and consistency"
pytest -m flow
```

也可以使用脚本：

```powershell
.\scripts\run_tests.ps1 -Suite smoke
.\scripts\run_tests.ps1 -Suite logs
.\scripts\run_tests.ps1 -Suite books
.\scripts\run_tests.ps1 -Suite db
.\scripts\run_tests.ps1 -Suite flow
.\scripts\run_tests.ps1 -Suite all
```

## Allure 报告说明

所有测试用例均使用：

- `allure.feature`
- `allure.story`
- `allure.title`

报告中可查看：

- 测试模块分组。
- 每条用例标题和执行结果。
- HTTP 请求信息。
- HTTP 响应信息。
- 异常断言失败信息。
- skipped 用例原因。

生成报告：

```powershell
pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
```

`allure-results/` 和 `allure-report/` 已加入忽略规则，不应提交。

## SQLite 数据一致性校验

`common/db_client.py` 使用 Python `sqlite3` 直连本地 SQLite 数据库。

数据库路径从环境变量 `SQLITE_DB_PATH` 读取，默认示例：

```env
SQLITE_DB_PATH=../backend/prisma/prisma/dev.db
```

已封装能力：

- 根据 ISBN 查询 `Book`。
- 根据 id 查询 `AuditLog`。
- 根据 action/entity/entityId 查询 `AuditLog`。
- 查询最近一条 `AuditLog`。

一致性测试示例：

- `GET /api/logs` 返回的日志，与数据库 `AuditLog` 记录比对 `action/entity/entityId/detail`。
- `GET /books` 返回的图书，与数据库 `Book` 记录比对 `title/author/isbn`。

如果数据库文件不存在，相关测试会使用 `pytest.skip` 跳过。

## 测试数据工厂与清理策略

`common/data_factory.py` 提供测试数据构造能力：

- 生成随机 ISBN。
- 生成唯一 title。
- 生成测试图书 payload。

测试数据统一使用 `TEST_AUTO_` 前缀，例如：

```text
TEST_AUTO_Book_...
TEST_AUTO_ISBN_...
```

`DbClient.delete_test_books_by_prefix()` 只允许清理 `TEST_AUTO_` 前缀数据，避免误删真实数据。

当前后端没有图书创建接口，因此创建图书完整流程测试目前为 skip，不夸大为已实现的写接口自动化。

## 当前测试范围

| 范围 | 覆盖内容 | 状态 |
| --- | --- | --- |
| health | `GET /health` 服务可用性检查 | 已实现 |
| logs | `GET /api/logs` 契约、分页、筛选、参数校验 | 已实现 |
| books | `GET /books`、`GET /books/:id` 契约和异常 id | 已实现 |
| db consistency | 接口响应与 SQLite 中 `Book`、`AuditLog` 记录一致性 | 已实现，依赖本地数据 |
| flow | 测试数据工厂；创建图书流程因无写接口跳过 | 部分实现，创建流 skip |

## 当前本地验证结果

本地执行：

```powershell
pytest -v
```

结果：

```text
16 items collected
14 passed
2 skipped
```

skipped 原因：

- 当前数据库无 audit log，日志数据库一致性用例跳过。
- 当前后端无图书创建接口，创建图书流程用例跳过。

## 已发现并改进的问题

在扩展接口测试工程过程中，发现并完成了以下改进：

| 问题 | 改进 |
| --- | --- |
| 实际日志接口只有 `/logs`，测试工程需要 `/api/logs` | 后端保留 `/logs`，新增 `/api/logs` |
| 日志接口原本直接返回数组 | 统一为 `items + pagination` 结构 |
| 日志接口缺少分页参数校验 | 增加 `limit`、`offset`、`userId` 参数校验 |
| 日志 user 可能暴露过多字段 | user 只返回 `id/name/email/role` |
| 图书列表缺少数据库一致性所需 ISBN | `GET /books` 列表补充 `isbn` 字段 |

## 本地运行命令

启动后端：

```powershell
cd D:\library-project\library-management-system\backend
npm run dev
```

准备测试环境：

```powershell
cd D:\library-project\library-management-system\api-tests
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

运行全部测试：

```powershell
pytest -v
```

运行分层测试：

```powershell
pytest -m smoke
pytest -m "logs and contract"
pytest -m "books and contract"
pytest -m "db and consistency"
pytest -m flow
```

生成 Allure 结果：

```powershell
pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## 简历项目描述

基于图书馆管理系统课程项目，独立扩展 Python 接口自动化测试工程，使用 pytest、requests、Allure 和 SQLite 完成健康检查、系统日志、图书信息、异常参数和数据库一致性校验，封装统一 RequestClient、断言工具、数据库查询工具和测试数据工厂，并通过 marker 分层执行和 Allure 请求/响应附件提升测试报告可观测性。

## 主要工作

- 搭建 `api-tests/` Python 接口自动化测试工程。
- 封装 `RequestClient`，统一请求、响应解析、token 设置和 Allure 附件。
- 为日志接口补充 `/api/logs` 路径、分页结构、参数校验和敏感字段控制。
- 编写 health、logs、books 多模块接口测试。
- 增加 SQLite 数据一致性校验，覆盖接口返回与数据库记录比对。
- 增加测试数据工厂和 `TEST_AUTO_` 安全清理策略。
- 使用 pytest marker 支持 smoke、contract、negative、db consistency、flow 分层执行。
- 编写项目展示文档和本地运行说明，便于简历展示和面试讲解。
