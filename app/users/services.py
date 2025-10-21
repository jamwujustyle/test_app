from sqlalchemy.ext.asyncio import AsyncSession
from .repositories import UserRepo


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepo(db)
