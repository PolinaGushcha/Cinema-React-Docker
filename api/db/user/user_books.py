import datetime
import uuid

from pydantic import BaseModel


class UserBookFilm(BaseModel):
    cinema_id: uuid.UUID
    cinema_name: str
    film_id: uuid.UUID
    film_name: str
    time: datetime.datetime
    seats: list[int]


class UserBooks(BaseModel):
    user_name: str
    books: list[UserBookFilm]
