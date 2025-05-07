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
