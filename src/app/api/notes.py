from typing import List
from fastapi import APIRouter, HTTPException

from app.api import crud
from app.api.models import NoteSchema, NoteDB


router = APIRouter()


@router.post("", response_model=NoteDB, status_code=201)
async def create_note(payload: NoteSchema):
    """
    Create a new note.
    """
    note = await crud.post(payload)
    return note


@router.get("/{note_id}", response_model=NoteDB)
async def read_note(note_id: int):
    """
    Get a note by ID.
    """
    note = await crud.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("", response_model=List[NoteDB])
async def read_all_notes():
    """
    Get all notes.
    """
    notes = await crud.get_all()
    return notes
