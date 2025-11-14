import uuid
from datetime import datetime

from citext import CIText
from sqlalchemy import true, Column, text
from sqlalchemy.sql.sqltypes import String, TIMESTAMP
from sqlmodel import SQLModel, Field


class User(SQLModel, table=true):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(sa_column=Column(String(100), nullable=False))
    last_name: str = Field(sa_column=Column(String(100), nullable=False))
    email: str = Field(sa_column=Column(CIText, unique=True))
    password_hash: str
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP')))
    updated_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'),
                         onupdate=text('CURRENT_TIMESTAMP')))
