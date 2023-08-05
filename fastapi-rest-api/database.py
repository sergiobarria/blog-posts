from typing import List

import databases
import sqlalchemy
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./data.db"

metadata = sqlalchemy.MetaData()

books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("author", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Float),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)

db = databases.Database(DATABASE_URL)


class BookIn(BaseModel):
    title: str
    author: str
    description: str
    price: float


class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    price: float


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    description: str | None = None
    price: float | None = None
