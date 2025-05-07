from fastapi import APIRouter, HTTPException

from app.api import crud
from app.api.models import NoteSchema, NoteDB


router = APIRouter()


@router.post("/notes", response_model=NoteDB, status_code=201)
async def create_note(payload: NoteSchema):
    """
    Create a new note.
    """
    try:
        note = await crud.post(payload)
        return note
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
