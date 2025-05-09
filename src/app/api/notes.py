from typing import List
from fastapi import APIRouter, HTTPException, Path

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


@router.get("/{note_id}", response_model=NoteDB, status_code=200)
async def read_note(
    note_id: int = Path(
        ...,
        gt=0,
        title="The ID of the note to get",
        description="Must be a positive integer",
    ),
):
    """
    Get a note by ID.
    """
    note = await crud.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("", response_model=List[NoteDB], status_code=200)
async def read_all_notes():
    """
    Get all notes.
    """
    notes = await crud.get_all()
    return notes


@router.put("/{note_id}", response_model=NoteDB, status_code=200)
async def update_note(note_id: int, payload: NoteSchema):
    """
    Update a note by ID.
    """
    note = await crud.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    updated_note = await crud.put(note_id, payload)
    return updated_note


@router.delete("/{note_id}", response_model=NoteDB, status_code=200)
async def delete_note(note_id: int):
    """
    Delete a note by ID.
    """
    note = await crud.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    await crud.delete(note_id)
    return note
