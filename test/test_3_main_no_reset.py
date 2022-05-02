import unittest
from unittest.mock import patch, MagicMock

from starlette.testclient import TestClient


from app.dao.book_dao import BookDao
from app.model.book import Book


class TestMain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.book_dao = MagicMock(BookDao)
        with patch("app.dao.book_dao.BookDao", return_value=cls.book_dao):
            from app.main import app
            cls.client = TestClient(app)

    def test_when_creating_book_then_dao_save_is_called_and_its_return_value_returned(
            self,
    ):
        book = _get_default_book()
        self.book_dao.save.return_value = book.id

        response = self.client.post("book", data=book.json())

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.json(), book.id)
        self.book_dao.save.assert_called_with(book)

    def test_when_getting_book_by_id_then_dao_get_by_id_called(
                self,
        ):
        book = _get_default_book()
        self.book_dao.get_by_id.return_value = book

        response = self.client.get(f"book/{book.id}")

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json(), book)
        self.book_dao.get_by_id.assert_called_with(book.id)

    def test_when_getting_book_by_id_then_dao_get_by_id_called_once(
            self,
    ):
        self.book_dao.get_by_id.return_value = _get_default_book()

        self.client.get(f"book/non_default_id")

        print(self.book_dao.get_by_id.call_count, self.book_dao.get_by_id.call_args_list)
        # prints 2 ,[call('id'), call('non_default_id')]
        self.assertEquals(self.book_dao.get_by_id.call_count, 1)  # AssertionError: 2 != 1


def _get_default_book():
    return Book(id="id", name="name")

