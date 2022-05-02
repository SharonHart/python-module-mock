import unittest
from unittest.mock import patch

from starlette.testclient import TestClient

from app.main import app
from app.model.book import Book


@patch("app.dao.book_dao.BookDao")
class TestMain(unittest.TestCase):

    def test_when_creating_book_then_dao_save_is_called_and_its_return_value_returned(
            self, book_dao
    ):
        book = _get_default_book()
        book_dao.save.return_value = book.id
        client = TestClient(app)

        response = client.post("book", data=book.json())

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.json(), book.id)
        book_dao.save.assert_called_with(book)


def _get_default_book():
    return Book(id="id", name="name")

