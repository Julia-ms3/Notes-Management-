from pydantic import BaseModel


class NoteAddSchema(BaseModel):
    header: str
    description: str


class Note(NoteAddSchema):
    id: int
