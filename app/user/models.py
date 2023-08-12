from datetime import datetime
from sqlalchemy import TIMESTAMP, Column, Integer, String, Table, Index, Boolean

from app.database import metadata

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", String, nullable=False),
    Column("nickname", String, nullable=False),
    Column("password_hash", String, nullable=False),
    Column("comment", String, nullable=True),
    Column("deleted", Boolean, default=False, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.now),
    Index("user_id", "user_id", unique = False)
)
