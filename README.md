# 图书馆管理系统接口自动化测试项目

## 项目定位

本仓库基于图书馆管理系统课程项目，扩展了一套面向测试开发实习展示的接口自动化测试工程，重点展示接口自动化测试、日志审计回归测试、数据库一致性校验、Allure 报告和基础 CI 回归能力。

项目保留原有图书馆管理系统作为被测系统，在此基础上新增 `api-tests/` 测试工程，用于验证后端接口的可用性、响应契约、异常参数、审计日志返回结构，以及接口响应与 SQLite 数据库记录的一致性。

## 测试开发项目亮点

- 使用 Python + pytest + requests 搭建 `api-tests/` 接口自动化测试工程
- 封装 `RequestClient`，统一请求、响应解析和 Allure 附件
- 覆盖 health、logs、books 接口测试
- 支持 contract、negative、db consistency、flow 分层测试
- 使用 SQLite 校验接口响应与数据库记录一致性
- 使用 `TEST_AUTO_` 构造和清理测试数据
- 接入 GitHub Actions 执行基础 CI 回归

## 本地验证结果

```powershell
pytest -v
```

当前结果：

```text
16 collected / 15 passed / 1 skipped
```

唯一 skipped 原因：当前后端没有图书写接口，因此创建图书完整流程用例跳过。

## 项目入口

- 详细测试项目说明：[API_TESTING_README.md](./API_TESTING_README.md)
- 测试工程目录：[api-tests/](./api-tests)
- 测试运行说明：[api-tests/README.md](./api-tests/README.md)
- CI 配置：[.github/workflows/api-tests.yml](./.github/workflows/api-tests.yml)

## 快速运行

启动后端：

```powershell
cd backend
```

```powershell
npm install
```

```powershell
npm run dev
```

运行接口自动化测试：

```powershell
cd api-tests
```

```powershell
python -m venv .venv
```

```powershell
.\.venv\Scripts\Activate.ps1
```

```powershell
pip install -r requirements.txt
```

```powershell
pytest -v
```

## 原系统说明

原项目为图书馆管理系统课程项目，采用前后端分离结构：

- 前端技术栈：React、Vite、Tailwind CSS
- 后端技术栈：Node.js、Express、Prisma、SQLite
- 原系统功能概述：图书信息、用户管理、借阅管理、系统日志等图书馆管理场景

当前测试开发扩展主要关注后端接口质量验证；不会把图书创建流程写成已完成闭环，相关用例在后端无写接口时保持 skip。
