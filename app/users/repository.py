from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from uuid import UUID
from typing import Optional

from .models import User, UserStatus


class UserRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(
        self, email: str, password: str, name: str = None, surname: str = None
    ) -> User:
        result = User(email=email, name=name, surname=surname)

        result.set_password(password)

        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)

        return result

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        user = await self.db.execute(select(User).where(User.id == user_id))

        return user.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.get_user_by_email(email)
        if user and user.verify_password(password):
            return user
        return None

    async def verify_user(self, user: User) -> User:
        user.status = UserStatus.VERIFIED
        user.verification_code = None
        user.verification_code_expires = None

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def update_verification_code(self, user: User) -> User:
        await self.db.commit()
        await self.db.refresh(user)
