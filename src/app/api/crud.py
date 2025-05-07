from app.api.models import NoteSchema
from app.db import database, notes


async def post(payload: NoteSchema):
    query = notes.insert().values(
        title=payload.title, description=payload.description
    )
    note_id = await database.execute(query=query)
    get_query = notes.select().where(notes.c.id == note_id)
    note = await database.fetch_one(query=get_query)
    return note
