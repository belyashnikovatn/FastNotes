import os

from sqlalchemy import (
    create_engine,
    MetaData,
    DateTime,
    Column,
    Integer,
    String,
    Table,
)
from sqlalchemy.sql import func
from databases import Database


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50), nullable=False),
    Column("description", String(50), nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
)

database = Database(DATABASE_URL)
