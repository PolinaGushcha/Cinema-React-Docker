import uuid

from pydantic import BaseModel

from .cinema import Cinema
from .film import Film


class CinemasByFilm(BaseModel):
    city_id: uuid.UUID | None
    film: Film | None
    cinemas: list[Cinema]
