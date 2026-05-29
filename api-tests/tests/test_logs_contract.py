import allure
import pytest

from common.assertions import (
    assert_log_item_fields,
    assert_pagination,
    assert_status_code,
)
from common.request_client import RequestClient


pytestmark = [
    pytest.mark.logs,
    pytest.mark.contract,
    pytest.mark.regression,
]


@allure.feature("Audit Logs")
@allure.story("Logs contract")
@allure.title("GET /api/logs returns items and pagination")
def test_get_logs_contract():
    client = RequestClient()

    response = client.get("/api/logs")

    assert_status_code(response, 200)
    body = response["body"]
    assert isinstance(body, dict), "logs response should be an object"
    assert "items" in body, "logs response should contain items"
    assert "pagination" in body, "logs response should contain pagination"
    assert isinstance(body["items"], list), "items should be a list"
    assert_pagination(body["pagination"], expected_limit=10, expected_offset=0)

    for log_item in body["items"]:
        assert_log_item_fields(log_item)
        assert_log_user_is_safe(log_item)


@allure.feature("Audit Logs")
@allure.story("Logs pagination")
@allure.title("GET /api/logs supports limit and offset")
def test_get_logs_with_pagination_params():
    client = RequestClient()
    limit = 5
    offset = 0

    response = client.get("/api/logs", params={"limit": limit, "offset": offset})

    assert_status_code(response, 200)
    body = response["body"]
    assert isinstance(body, dict), "logs response should be an object"
    assert isinstance(body.get("items"), list), "items should be a list"
    assert len(body["items"]) <= limit
    assert_pagination(body.get("pagination"), expected_limit=limit, expected_offset=offset)

    for log_item in body["items"]:
        assert_log_item_fields(log_item)
        assert_log_user_is_safe(log_item)


@allure.feature("Audit Logs")
@allure.story("Logs filtering")
@allure.title("GET /api/logs supports action filter")
def test_get_logs_with_action_filter():
    client = RequestClient()
    action = "LOGIN"

    response = client.get("/api/logs", params={"action": action})

    assert_status_code(response, 200)
    body = response["body"]
    assert isinstance(body, dict), "logs response should be an object"
    assert isinstance(body.get("items"), list), "items should be a list"
    assert_pagination(body.get("pagination"))

    for log_item in body["items"]:
        assert_log_item_fields(log_item)
        assert_log_user_is_safe(log_item)
        assert log_item["action"] == action


def assert_log_user_is_safe(log_item):
    user = log_item.get("user")

    if user is None:
        return

    assert set(user.keys()) <= {"id", "name", "email", "role"}
    assert "passwordHash" not in user
    assert "password" not in user
