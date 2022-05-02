import uvicorn
from fastapi import FastAPI

from app.dao.book_dao import BookDao
from app.model.book import Book

app = FastAPI()
book_dao = BookDao()


@app.post("/book", status_code=201)
async def create_book(book: Book):
    return book_dao.save(book)


@app.get("/book/{book_id}")
async def get_book(book_id: str):
    return book_dao.get_by_id(book_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
