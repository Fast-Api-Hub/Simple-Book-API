from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException, Body
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published: int

    def __init__(self, id, title, author, description, rating, published):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published = published

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published: int = Field(gt=-1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "new book",
                "author": "author",
                "description": "description of book",
                "rating": 5,
                "published": 2029,
            }
        }
    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]

### GET
@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_return = []

    for book in BOOKS:
        if book.rating == book_rating:
            books_return.append(book)

    return books_return

@app.get("/books/published/", status_code=status.HTTP_200_OK)
async def read_book_by_published(published: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published == published:
            books_to_return.append(book)
    return books_to_return

### POST
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

### PUT
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_change = True

    if not book_change:
        raise HTTPException(status_code=404, detail="Book not found")


### DELETE
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_change = False

    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_change = True
            break

    if not book_change:
        raise HTTPException(status_code=404, detail="Book not found")