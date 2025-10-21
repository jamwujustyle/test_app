from fastapi.routing import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_db
from app.config.dependencies import get_current_user

from .schemas import UserResponse
from .models import User

router = APIRouter(prefix="/users")


@router.get("/me", response_model=UserResponse)
async def me(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return current_user
