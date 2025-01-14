import uuid

from pydantic import BaseModel


class City(BaseModel):
    id: uuid.UUID
    name: str
    add_info: str
