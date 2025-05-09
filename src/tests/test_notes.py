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

    response = test_app.post(
        "/notes",
        content=json.dumps({"title": "Test Note"}),
    )
    assert response.status_code == 422

    response = test_app.post(
        "/notes",
        content=json.dumps({"title": "1", "description": "2"}),
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

    response = test_app.get("/notes/0")
    assert response.status_code == 422

    response = test_app.get("/notes/abc")
    assert response.status_code == 422


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


def test_update_note_success(test_app, monkeypatch):
    async def mock_get(note_id):
        return NoteDB(
            id=1,
            title="Test Note",
            description="This is a test note.",
            created_at=datetime(2023, 10, 1, 0, 0),
        )

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(note_id, payload):
        return NoteDB(
            id=1,
            title=payload.title,
            description=payload.description,
            created_at=datetime(2023, 10, 1, 0, 0),
        )

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(
        "/notes/1",
        json={
            "title": "Updated Note",
            "description": "This is an updated test note.",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Updated Note",
        "description": "This is an updated test note.",
        "created_at": "2023-10-01T00:00:00",
    }


@pytest.mark.parametrize(
    "note_id, payload, status_code",
    [
        (1, {}, 422),
        (1, {"description": "bar"}, 422),
        (999, {"title": "foo", "description": "bar"}, 404),
        (1, {"title": "1", "description": "123"}, 422),
        (1, {"title": "123", "description": "1"}, 422),
        (0, {"title": "foo", "description": "bar."}, 422),
        ("abc", {"title": "foo", "description": "bar"}, 422),
    ],
)
def test_update_note_invalid(
    test_app, monkeypatch, note_id, payload, status_code
):
    async def mock_get(note_id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(
        f"/notes/{note_id}",
        json=payload,
    )
    assert response.status_code == status_code


def test_delete_note_success(test_app, monkeypatch):
    async def mock_get(note_id):
        return NoteDB(
            id=1,
            title="Test Note",
            description="This is a test note.",
            created_at=datetime(2023, 10, 1, 0, 0),
        )

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(note_id):
        return NoteDB(
            id=1,
            title="Test Note",
            description="This is a test note.",
            created_at=datetime(2023, 10, 1, 0, 0),
        )

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/notes/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Test Note",
        "description": "This is a test note.",
        "created_at": "2023-10-01T00:00:00",
    }


def test_delete_note_not_found(test_app, monkeypatch):
    async def mock_get(note_id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/notes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Note not found"}

    response = test_app.delete("/notes/0")
    assert response.status_code == 422
