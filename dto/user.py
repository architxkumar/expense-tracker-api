from pydantic import EmailStr, BaseModel
from sqlmodel import SQLModel, Field

# FIX: Replace with pydnantic's BaseModel to reserve SQLModel for DB models only
class UserCreate(SQLModel):
    model_config = {"extra": "forbid"}
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
