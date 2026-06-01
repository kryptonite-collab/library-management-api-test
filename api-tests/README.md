# API Tests

Python interface automation tests for the local library management backend.

## Create Virtual Environment

```bash
cd api-tests
python -m venv .venv
```

Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment

Copy `.env.example` to `.env` and adjust values if needed:

```bash
copy .env.example .env
```

Default configuration:

```env
BASE_URL=http://localhost:3001
REQUEST_TIMEOUT=10
SQLITE_DB_PATH=../backend/prisma/prisma/dev.db
```

## Start Backend

Open another terminal:

```bash
cd ..\backend
npm run dev
```

Verify the service is available:

```bash
curl http://localhost:3001/health
```

## Run Pytest

Run all tests:

```bash
pytest
```

Run smoke tests:

```bash
pytest -m smoke
```

Run log contract tests:

```bash
pytest -m "logs and contract"
```

Run book contract tests:

```bash
pytest -m "books and contract"
```

Run database consistency tests:

```bash
pytest -m "db and consistency"
```

Run flow tests:

```bash
pytest -m flow
```

Run with the helper script:

```bash
.\scripts\run_tests.ps1 -Suite smoke
.\scripts\run_tests.ps1 -Suite logs
.\scripts\run_tests.ps1 -Suite books
.\scripts\run_tests.ps1 -Suite db
.\scripts\run_tests.ps1 -Suite flow
.\scripts\run_tests.ps1 -Suite all
```

## Test Scope

- `smoke`: verifies backend service availability through `GET /health`.
- `logs`: verifies system log list, pagination, filtering, and invalid parameter handling through `GET /api/logs`.
- `books`: verifies book list and detail contracts through `GET /books` and `GET /books/:id`.
- `db` and `consistency`: compares API responses with local SQLite `Book` and `AuditLog` records.
- `flow`: covers data factory readiness and future write-flow scenarios.

## Database Consistency Tests

Database consistency tests read the local SQLite database directly with Python `sqlite3`.

Configure the database path in `.env` when your local path differs:

```env
SQLITE_DB_PATH=../backend/prisma/prisma/dev.db
```

Run only consistency tests:

```bash
pytest -m "db and consistency"
```

If the SQLite file does not exist, related tests are skipped instead of failed.

The audit log consistency test now creates its own `TEST_AUTO_` audit log before calling `GET /api/logs`, compares the API response with the SQLite `AuditLog` row, and cleans the test log after the assertion. It no longer depends on pre-existing audit log data.

## Test Data Construction and Cleanup

`common/data_factory.py` provides reusable builders for automated test data:

- Random test ISBN values.
- Unique test book titles.
- Full test book payloads.
- TEST_AUTO_ audit log records for consistency tests.

Generated test data uses the `TEST_AUTO_` prefix for book `title`, book `isbn`, and audit log `detail`.

后端已提供带馆员鉴权的图书写接口；当前自动化尚未接入馆员登录、创建、详情校验、数据库校验和清理闭环，因此该流程暂时 skip。

- `GET /books`
- `GET /books/:id`

The automated flow does not create or delete real book records through HTTP yet. The existing coverage includes API contracts and database consistency checks.

For future write-flow tests, cleanup must only remove records whose `title` or `isbn` starts with `TEST_AUTO_`. `DbClient.delete_test_books_by_prefix()` enforces this guard to avoid deleting real data.

Audit log cleanup only removes records whose `detail` starts with `TEST_AUTO_`. `DbClient.delete_test_audit_logs_by_prefix()` enforces the same guard for audit log test data.

## 如何生成测试报告

Collect Allure results:

```bash
pytest --alluredir=allure-results
```

Or run all tests and collect results with the helper script:

```bash
.\scripts\run_tests.ps1 -Suite all
```

Generate and open the report:

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## 测试报告包含哪些信息

Allure report includes:

- Test module grouping by `feature`, `story`, and `title`.
- Request attachment: method, URL, masked headers, query params, and JSON body.
- Response attachment: status code and response body.
- Test markers for quick filtering, including `smoke`, `logs`, `books`, `db`, `consistency`, `flow`, `contract`, `regression`, and `negative`.
