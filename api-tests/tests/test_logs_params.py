import allure
import pytest

from common.assertions import assert_status_code
from common.request_client import RequestClient


pytestmark = [
    pytest.mark.logs,
    pytest.mark.negative,
    pytest.mark.regression,
]


@allure.feature("Audit Logs")
@allure.story("Logs parameter validation")
@allure.title("GET /api/logs rejects limit=0")
def test_get_logs_rejects_zero_limit():
    client = RequestClient()

    response = client.get("/api/logs", params={"limit": 0})

    assert_status_code(response, 400)


@allure.feature("Audit Logs")
@allure.story("Logs parameter validation")
@allure.title("GET /api/logs rejects negative limit")
def test_get_logs_rejects_negative_limit():
    client = RequestClient()

    response = client.get("/api/logs", params={"limit": -1})

    assert_status_code(response, 400)


@allure.feature("Audit Logs")
@allure.story("Logs parameter validation")
@allure.title("GET /api/logs rejects negative offset")
def test_get_logs_rejects_negative_offset():
    client = RequestClient()

    response = client.get("/api/logs", params={"offset": -1})

    assert_status_code(response, 400)


@allure.feature("Audit Logs")
@allure.story("Logs parameter validation")
@allure.title("GET /api/logs rejects non-numeric userId")
def test_get_logs_rejects_non_numeric_user_id():
    client = RequestClient()

    response = client.get("/api/logs", params={"userId": "abc"})

    assert_status_code(response, 400)
