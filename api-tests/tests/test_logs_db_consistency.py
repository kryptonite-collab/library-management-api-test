import allure
import pytest

from common.assertions import assert_status_code
from common.db_client import DbClient
from common.request_client import RequestClient


pytestmark = [
    pytest.mark.logs,
    pytest.mark.db,
    pytest.mark.consistency,
    pytest.mark.regression,
]


@allure.feature("Audit Logs")
@allure.story("Database consistency")
@allure.title("GET /api/logs response matches AuditLog database record")
def test_logs_response_matches_database_record():
    client = RequestClient()
    db = DbClient()

    response = client.get("/api/logs")

    assert_status_code(response, 200)
    items = response["body"].get("items", [])

    if not items:
        pytest.skip("No audit logs exist in the current database.")

    api_log = items[0]
    db_log = db.get_audit_log_by_id(api_log["id"])

    assert db_log is not None, f"AuditLog id={api_log['id']} should exist in database"
    assert api_log["action"] == db_log["action"]
    assert api_log["entity"] == db_log["entity"]
    assert api_log["entityId"] == db_log["entityId"]
    assert api_log["detail"] == db_log["detail"]
