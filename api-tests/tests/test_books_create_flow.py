import allure
import pytest

from common.data_factory import TEST_DATA_PREFIX, generate_test_book_payload


pytestmark = [
    pytest.mark.books,
    pytest.mark.flow,
    pytest.mark.regression,
]


@allure.feature("Books")
@allure.story("Test data factory")
@allure.title("Generate safe test book payload with TEST_AUTO_ prefix")
def test_generate_test_book_payload():
    payload = generate_test_book_payload()

    assert payload["title"].startswith(TEST_DATA_PREFIX)
    assert payload["isbn"].startswith(TEST_DATA_PREFIX)
    assert payload["author"]
    assert payload["genre"]


@allure.feature("Books")
@allure.story("Create book flow")
@allure.title("Create book flow is skipped until write API is available")
def test_create_book_flow_requires_write_api():
    payload = generate_test_book_payload()
    assert payload["title"].startswith(TEST_DATA_PREFIX)
    assert payload["isbn"].startswith(TEST_DATA_PREFIX)

    pytest.skip(
        "Current backend only exposes read-only book APIs: GET /books and GET /books/:id. "
        "Create/detail/database/cleanup flow can be enabled after a POST /books API exists."
    )
