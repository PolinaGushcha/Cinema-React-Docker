import uuid

from pydantic import BaseModel


class Cinema(BaseModel):
    id: uuid.UUID
    name: str
