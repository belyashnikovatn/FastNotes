import os

from database import Database
from sqlalchemy import create_engine, MetaData


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

database = Database(DATABASE_URL)
