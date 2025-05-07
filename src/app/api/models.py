from pydantic import BaseModel
from datetime import datetime


class NoteSchema(BaseModel):
    title: str
    description: str


class NoteDB(NoteSchema):
    id: int
    created_at: datetime
