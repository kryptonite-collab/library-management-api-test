import allure
import pytest

from common.assertions import assert_status_code
from common.db_client import DbClient
from common.request_client import RequestClient


pytestmark = [
    pytest.mark.books,
    pytest.mark.db,
    pytest.mark.consistency,
    pytest.mark.regression,
]


def _extract_books(response_body):
    if isinstance(response_body, dict) and "data" in response_body:
        return response_body["data"]

    if isinstance(response_body, list):
        return response_body

    pytest.fail("books response should be a list or an object with a data list")


@allure.feature("Books")
@allure.story("Database consistency")
@allure.title("GET /books response matches Book database record")
def test_books_response_matches_database_record():
    client = RequestClient()
    db = DbClient()

    response = client.get("/books")

    assert_status_code(response, 200)
    books = _extract_books(response["body"])

    if not books:
        pytest.skip("No books exist in the current database.")

    api_book = books[0]
    assert "isbn" in api_book, "book list item should contain isbn for database consistency checks"

    db_book = db.get_book_by_isbn(api_book["isbn"])

    assert db_book is not None, f"Book isbn={api_book['isbn']} should exist in database"
    assert api_book["title"] == db_book["title"]
    assert api_book["author"] == db_book["author"]
    assert api_book["isbn"] == db_book["isbn"]
