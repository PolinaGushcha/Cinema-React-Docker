import datetime
import uuid

from pydantic import BaseModel


class TimeSlot(BaseModel):
    cinema_id: uuid.UUID
    film_id: uuid.UUID
    time: datetime.datetime
