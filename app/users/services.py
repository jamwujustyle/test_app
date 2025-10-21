from sqlalchemy.ext.asyncio import AsyncSession

from .repository import UserRepo
from .models import User, UserStatus

from uuid import UUID
from typing import Optional


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepo(db)

    async def create_user(
        self, email: str, password: str, name: str = None, surname: str = None
    ):
        return await self.repo.create_user(
            email=email, password=password, name=name, surname=surname
        )

    async def get_user_by_id(self, user_id: UUID):
        return await self.repo.get_user_by_id(user_id)

    async def authenticate_user(self, email: str, password: str) -> User:
        return self.repo.authenticate_user(email=email, password=password)

    async def create_user_with_verification(
        self, email: str, password: str, name: str = None, surname: str = None
    ):
        user = await self.repo.create_user(
            email=email, password=password, name=name, surname=surname
        )

        code = user.generate_verification_code()
        await self.repo.update_verification_code(user)

        return user, code

    async def verify_user_email(self, email: str, code: str) -> Optional[User]:
        user = await self.repo.get_user_by_email(email)

        if not user:
            return None

        if user.status == UserStatus.VERIFIED:
            return user

        if not user.verify_code(code):
            return None

        return await self.repo.verify_user(user)

    async def resend_verification_code(self, email: str) -> Optional[tuple[User, str]]:
        user = await self.repo.get_user_by_email(email)

        if not user:
            return None

        if user.status == UserStatus.VERIFIED:
            return None

        code = user.generate_verification_code()
        await self.repo.update_verification_code(user)

        return user, code
