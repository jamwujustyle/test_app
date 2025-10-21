from sqlalchemy.ext.asyncio import AsyncSession

from .repository import UserRepo
from .models import User

from uuid import UUID


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
