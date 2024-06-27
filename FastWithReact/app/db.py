import os

from sqlalchemy import (Column, DateTime, Integer, String, Table, create_engine, MetaData)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from databases import Database

DATABASE_URL = "postgresql://postgres:root@localhost/fastapi"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
metadata = MetaData()

blogs = Table(
    "blogs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False)
)

database = Database(DATABASE_URL)