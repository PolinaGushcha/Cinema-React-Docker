import uuid

from pydantic import BaseModel


class Film(BaseModel):
    id: uuid.UUID
    name: str
