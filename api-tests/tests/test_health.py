import allure
import pytest

from common.assertions import assert_status_code
from common.request_client import RequestClient


@allure.feature("Health")
@allure.story("Service availability")
@allure.title("GET /health returns service availability")
@pytest.mark.smoke
def test_health_check():
    client = RequestClient()

    response = client.get("/health")

    assert_status_code(response, 200)
    body = response["body"]
    assert isinstance(body, dict), "health response should be an object"
    assert body.get("status") == "ok" or "running" in response["text"].lower()
