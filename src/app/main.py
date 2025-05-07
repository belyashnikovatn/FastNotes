from fastapi import FastAPI

from app.api import ping


app = FastAPI(title="FastNotes", version="0.1.0")
app.include_router(ping.router)
