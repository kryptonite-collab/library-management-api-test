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

## Test Scope

- `smoke`: verifies backend service availability through `GET /health`.
- `logs`: verifies system log list, pagination, filtering, and invalid parameter handling through `GET /api/logs`.
- `books`: verifies book list and detail contracts through `GET /books` and `GET /books/:id`.

## Generate Allure Report

Collect Allure results:

```bash
pytest --alluredir=allure-results
```

Generate and open the report:

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```
