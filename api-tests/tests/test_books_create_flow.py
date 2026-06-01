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
@allure.title("Create book flow is skipped until authenticated write-flow automation is added")
def test_create_book_flow_requires_write_api():
    payload = generate_test_book_payload()
    assert payload["title"].startswith(TEST_DATA_PREFIX)
    assert payload["isbn"].startswith(TEST_DATA_PREFIX)

    pytest.skip(
        "后端已提供带馆员鉴权的图书写接口；当前自动化尚未接入馆员登录、创建、详情校验、"
        "数据库校验和清理闭环，因此该流程暂时 skip。"
    )
