import bcrypt
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.models.user import Users
from dto.user import UserCreate


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, data: UserCreate):
        # Check if email exists
        result = await self.session.exec(
            select(Users).where(Users.email == data.email)
        )
        existing = result.first()

        if existing:
            raise ValueError("User with this email already exists")

        # Hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(data.password.encode(), salt).decode()

        # Create new user
        user = Users(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password_hash=hashed
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
