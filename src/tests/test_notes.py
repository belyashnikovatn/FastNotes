from datetime import datetime
import json

import pytest

from app.api import crud
from app.api.models import NoteDB


def test_create_note_success(test_app, monkeypatch):
    test_request_payload = {
        "title": "Test Note",
        "description": "This is a test note.",
    }
    test_response_payload = {
        "id": 1,
        "title": "Test Note",
        "description": "This is a test note.",
        "created_at": "2023-10-01T00:00:00",
    }

    async def mock_post(payload):
        return NoteDB(
            id=1,
            title=payload.title,
            description=payload.description,
            created_at=datetime(2023, 10, 1, 0, 0),
        )

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post(
        "/notes",
        json=test_request_payload,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_note_invalid_json(test_app):

    response = test_app.post(
        "/notes",
        content=json.dumps({}),
    )
    assert response.status_code == 422


def test_read_note_success(test_app, monkeypatch):
    test_response_payload = {
        "id": 1,
        "title": "Test Note",
        "description": "This is a test note.",
        "created_at": "2023-10-01T00:00:00",
    }

    async def mock_get(note_id):
        return NoteDB(
            id=1,
            title="Test Note",
            description="This is a test note.",
            created_at=datetime(2023, 10, 1, 0, 0),
        )

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/notes/1")
    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_read_note_not_found(test_app, monkeypatch):
    async def mock_get(note_id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/notes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Note not found"}


def test_read_all_notes_success(test_app, monkeypatch):
    async def mock_get_all():
        return [
            NoteDB(
                id=1,
                title="Test Note",
                description="This is a test note.",
                created_at=datetime(2023, 10, 1, 0, 0),
            )
        ]

    monkeypatch.setattr(crud, "get_all", mock_get_all)
    response = test_app.get("/notes")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Test Note",
            "description": "This is a test note.",
            "created_at": "2023-10-01T00:00:00",
        }
    ]


def test_read_all_notes_empty(test_app, monkeypatch):
    async def mock_get_all():
        return []

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/notes")
    assert response.status_code == 200
    assert response.json() == []
