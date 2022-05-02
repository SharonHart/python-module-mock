import os

from bson import ObjectId
from pymongo import MongoClient

from app.model.book import Book


class BookDao:

    def __init__(self):
        client = MongoClient(os.environ.get("DATABASE_CONNECTION_STRING", "mongodb://database:27017"))
        self.book_collection = client.app.book

    def save(self, book: Book) -> str:
        return self.book_collection.insert_one(book.dict()).inserted_id

    def get_by_id(self, book_id: str) -> Book:
        by_id_filter = {"_id": ObjectId(book_id)}
        return Book(**self.book_collection.find_one(by_id_filter))
