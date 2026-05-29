from typing import Optional


def assert_status_code(response: dict, expected_status_code: int) -> None:
    assert response["status_code"] == expected_status_code, (
        f"Expected status code {expected_status_code}, "
        f"got {response['status_code']}. Response body: {response['text']}"
    )

def assert_pagination(
    pagination: dict,
    expected_limit: Optional[int] = None,
    expected_offset: Optional[int] = None,
) -> None:
    assert isinstance(pagination, dict), "pagination should be an object"

    for field in ("limit", "offset", "total"):
        assert field in pagination, f"pagination should contain {field}"
        assert isinstance(pagination[field], int), f"pagination.{field} should be an integer"
        assert pagination[field] >= 0, f"pagination.{field} should be greater than or equal to 0"

    if expected_limit is not None:
        assert pagination["limit"] == expected_limit

    if expected_offset is not None:
        assert pagination["offset"] == expected_offset


def assert_log_item_fields(log_item: dict) -> None:
    assert isinstance(log_item, dict), "log item should be an object"

    required_fields = ("id", "action", "entity", "detail", "createdAt")
    for field in required_fields:
        assert field in log_item, f"log item should contain {field}"

    assert isinstance(log_item["id"], int), "log item id should be an integer"
    assert isinstance(log_item["action"], str), "log item action should be a string"
    assert isinstance(log_item["entity"], str), "log item entity should be a string"
    assert log_item["detail"] is None or isinstance(log_item["detail"], str), (
        "log item detail should be a string or null"
    )
    assert isinstance(log_item["createdAt"], str), "log item createdAt should be a string"
