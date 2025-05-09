
# 📝 FastNotes

**FastNotes** — это RESTful API-сервис для управления заметками, реализованный с использованием асинхронного стека. Проект поддерживает операции CRUD для работы с заметками и покрыт тестами.

## 🚀 Стек технологий

| Компонент     | Технология                             |
|---------------|-----------------------------------------|
| Backend       | [FastAPI](https://fastapi.tiangolo.com/) |
| ORM           | [SQLAlchemy (async)](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) |
| База данных   | [PostgreSQL](https://www.postgresql.org/) (через [Databases](https://www.encode.io/databases/)) |
| Тестирование  | [Pytest](https://docs.pytest.org/) + [HTTPX](https://www.python-httpx.org/) |
| Документация  | Автоматическая через FastAPI `/docs`   |
| Контейнеризация | [Docker](https://www.docker.com/) + [Docker Compose](https://docs.docker.com/compose/) |



## 🧪 Тестирование

Проект покрыт юнит-тестами с использованием:

- `pytest` — основной тестовый фреймворк.
- `monkeypatch` 

### 📌 Примеры тестов:

```python
def test_create_note_success(test_app, monkeypatch):
    async def mock_post(payload):
        return { "id": 1, "title": payload["title"], "description": payload["description"], "created_at": "..." }
    monkeypatch.setattr(crud, "post", mock_post)
    response = test_app.post("/notes", json={"title": "Test", "description": "..."})
    assert response.status_code == 201
```

## 🐳 Быстрый старт (через Docker)

1. Клонируйте репозиторий:
```bash
git clone https://github.com/belyashnikovatn/FastNotes.git
cd FastNotes
```

2. Запустите контейнеры:
```bash
docker-compose up --build
```

3. Откройте документацию:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

4. Запустите тесты:
```bash
docker compose exec web pytest .
```
