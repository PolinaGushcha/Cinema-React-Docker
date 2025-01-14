import datetime
import uuid
from enum import Enum

from pydantic import BaseModel


class BookStatus(str, Enum):
    BOOKED = "booked"
    AVAILABLE = "available"

    @classmethod
    def from_bool(cls, is_booked: bool) -> "BookStatus":
        return cls.BOOKED if is_booked else cls.AVAILABLE

    @property
    def is_booked(self) -> bool:
        return self == self.BOOKED


class Seat(BaseModel):
    seat_number: int
    book_status: BookStatus


class SeatBookStatus(BaseModel):
    cinema_id: uuid.UUID | None
    film_id: uuid.UUID | None
    time: datetime.datetime | None
    seats: list[Seat]
