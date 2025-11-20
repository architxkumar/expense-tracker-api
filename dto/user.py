from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class UserCreate(SQLModel):
    model_config = {"extra": "forbid"}
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
