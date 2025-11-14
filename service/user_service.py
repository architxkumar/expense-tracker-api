import bcrypt
from sqlmodel import Session, select

from db.models.user import User
from dto.user import UserCreate


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, data: UserCreate):
        existing = self.session.exec(
            select(User).where(User.email == data.email)
        ).first()

        # Check if user with the same email already exists
        if existing:
            raise ValueError("User with this email already exists")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(data.password.encode('utf-8'), salt)

        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password_hash=hashed.decode('utf-8')
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)







