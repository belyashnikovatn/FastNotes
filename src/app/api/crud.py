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


async def get(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    note = await database.fetch_one(query=query)
    return note


async def get_all():
    query = notes.select()
    notes_list = await database.fetch_all(query=query)
    return notes_list


async def put(note_id: int, payload: NoteSchema):
    query = (
        notes.update()
        .where(notes.c.id == note_id)
        .values(title=payload.title, description=payload.description)
        .returning(
            notes.c.id, notes.c.title, notes.c.description, notes.c.created_at
        )
    )
    updated_note = await database.fetch_one(query=query)
    return updated_note
