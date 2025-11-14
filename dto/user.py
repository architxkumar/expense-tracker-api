from sqlmodel import SQLModel


class UserCreate(SQLModel):
    first_name: str
    last_name: str
    email: str
    password: str

