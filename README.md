# 图书馆管理系统接口自动化测试项目

本仓库基于图书馆管理系统课程项目，扩展了一套面向测试开发实习展示的接口自动化测试工程，重点展示接口自动化测试、日志审计回归测试、数据库一致性校验、Allure 报告和基础 CI 回归能力。

## 测试开发项目亮点

- 使用 Python + pytest + requests 搭建 `api-tests/` 接口自动化测试工程
- 封装 `RequestClient`，统一管理 base_url、timeout、请求方法、响应解析和 Allure 请求/响应附件
- 覆盖 `health`、`logs`、`books` 等接口测试场景
- 支持 contract、negative、db consistency、flow 等分层测试
- 使用 SQLite 校验接口响应与数据库记录一致性
- 使用 `TEST_AUTO_` 前缀构造和清理自动化测试数据
- 接入 GitHub Actions 执行基础 CI 回归

## 本地验证结果

```text
pytest -v
16 collected / 15 passed / 1 skipped

唯一 skipped 原因：当前后端没有图书写接口，因此创建图书完整流程用例跳过。

项目入口
详细测试项目说明：API_TESTING_README.md
测试工程目录：api-tests/
测试运行说明：api-tests/README.md
CI 配置：.github/workflows/api-tests.yml
快速运行

启动后端：

cd backend
npm install
npm run dev

运行接口自动化测试：

cd api-tests
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v

生成 Allure 结果：

pytest --alluredir=allure-results
原系统说明

原项目为图书馆管理系统课程项目，采用前后端分离结构：

层级	技术
前端	React、Vite、Tailwind CSS
后端	Node.js、Express、Prisma
数据库	SQLite
测试扩展	Python、pytest、requests、Allure、SQLite

原系统包含图书信息、用户管理、系统日志等模块。本次个人扩展重点放在后端接口自动化测试与日志审计回归测试，不改动前端展示逻辑。
