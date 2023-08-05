from typing import List

from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from database import db, books, Book, BookIn, BookUpdate

app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
def home():
    return {"Hello": "World"}


@app.post("/books", response_model=Book, status_code=201)
async def create_book(book: BookIn):
    query = books.insert().values(
        title=book.title,
        author=book.author,
        description=book.description,
        price=book.price,
    )
    last_record_id = await db.execute(query)
    return {**book.model_dump(), "id": last_record_id}


@app.get("/books", response_model=List[Book])
async def get_books():
    query = books.select()
    return await db.fetch_all(query)


@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    query = books.select().where(books.c.id == book_id)
    book_record = await db.fetch_one(query)

    if not book_record:
        raise HTTPException(status_code=404, detail="Book not found")

    return book_record


@app.patch("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book: BookUpdate):
    book_query = books.select().where(books.c.id == book_id)
    book_record = await db.fetch_one(book_query)

    if not book_record:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book.model_dump(exclude_unset=True)
    updated_book = dict(book_record)
    updated_book.update(update_data)

    query = books.update().where(books.c.id == book_id).values(**update_data)
    await db.execute(query)

    updated_book_query = books.select().where(books.c.id == book_id)
    updated_book_record = await db.fetch_one(updated_book_query)
    return updated_book_record


@app.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: int):
    query = books.delete().where(books.c.id == book_id)
    await db.execute(query)
    return None
