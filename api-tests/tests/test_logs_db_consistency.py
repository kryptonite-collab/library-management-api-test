import allure
import pytest

from common.assertions import assert_status_code
from common.data_factory import generate_test_audit_log_data
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

    db.delete_test_audit_logs_by_prefix()
    test_log_data = generate_test_audit_log_data()
    inserted_log = db.insert_test_audit_log(test_log_data)

    try:
        response = client.get("/api/logs", params={"action": inserted_log["action"]})

        assert_status_code(response, 200)
        items = response["body"].get("items", [])
        api_log = next(
            (item for item in items if item.get("detail") == inserted_log["detail"]),
            None,
        )

        assert api_log is not None, "Inserted TEST_AUTO_ audit log should be returned by API"

        db_log = db.get_audit_log_by_id(api_log["id"])

        assert db_log is not None, f"AuditLog id={api_log['id']} should exist in database"
        assert api_log["action"] == db_log["action"]
        assert api_log["entity"] == db_log["entity"]
        assert api_log["entityId"] == db_log["entityId"]
        assert api_log["detail"] == db_log["detail"]
    finally:
        db.delete_test_audit_logs_by_prefix()
