import datetime
import uuid

from pydantic import BaseModel


class TimesByCinemaFilm(BaseModel):
    cinema_id: uuid.UUID
    cinema_name: str
    film_id: uuid.UUID
    film_name: str
    times: list[datetime.datetime]
