import allure
import pytest

from common.assertions import assert_status_code
from common.request_client import RequestClient


pytestmark = [
    pytest.mark.books,
    pytest.mark.contract,
    pytest.mark.regression,
]


def _extract_books(response_body):
    if isinstance(response_body, dict) and "data" in response_body:
        assert isinstance(response_body["data"], list), "books response data should be a list"
        return response_body["data"]

    if isinstance(response_body, list):
        return response_body

    pytest.fail("books response should be a list or an object with a data list")


def _assert_book_detail_fields(book):
    assert isinstance(book, dict), "book detail should be an object"

    for field in ("id", "title", "author", "isbn"):
        assert field in book, f"book detail should contain {field}"

    assert isinstance(book["id"], int), "book id should be an integer"
    assert isinstance(book["title"], str), "book title should be a string"
    assert isinstance(book["author"], str), "book author should be a string"
    assert isinstance(book["isbn"], str), "book isbn should be a string"


@allure.feature("Books")
@allure.story("Books contract")
@allure.title("GET /books returns a compatible books list structure")
def test_get_books_contract():
    client = RequestClient()

    response = client.get("/books")

    assert_status_code(response, 200)
    books = _extract_books(response["body"])
    assert isinstance(books, list), "books should be a list"


@allure.feature("Books")
@allure.story("Book detail")
@allure.title("GET /books/{id} returns book detail for the first book")
def test_get_book_detail_by_first_book_id():
    client = RequestClient()

    list_response = client.get("/books")
    assert_status_code(list_response, 200)
    books = _extract_books(list_response["body"])

    if not books:
        pytest.skip("No books exist in the current database.")

    book_id = books[0]["id"]
    detail_response = client.get(f"/books/{book_id}")

    assert_status_code(detail_response, 200)
    _assert_book_detail_fields(detail_response["body"])
    assert detail_response["body"]["id"] == book_id


@allure.feature("Books")
@allure.story("Book detail validation")
@allure.title("GET /books/abc rejects an invalid book id")
def test_get_book_detail_with_invalid_id():
    client = RequestClient()

    response = client.get("/books/abc")

    assert_status_code(response, 400)


@allure.feature("Books")
@allure.story("Book detail validation")
@allure.title("GET /books/99999999 returns not found")
def test_get_book_detail_with_missing_id():
    client = RequestClient()

    response = client.get("/books/99999999")

    assert_status_code(response, 404)
