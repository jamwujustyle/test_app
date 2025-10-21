from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_db
from app.config.dependencies import get_current_user

from .schemas import UserResponse, UserListResponse, UserUpdate
from .models import User, UserRole
from .services import AdminService, UserService

router = APIRouter(prefix="/users")


@router.get("/me", response_model=UserResponse)
async def me(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return current_user


# :! **************ADMIN ROUTES*****************
# _______________________________________________


@router.get("/", response_model=UserListResponse)
async def users(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):

    check_perm(current_user)
    users = await AdminService(db).fetch_all_users()
    return {"users": users}


@router.get("/{user_id}", response_model=UserResponse)
async def retrieve_user(
    user_id,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    check_perm(current_user)
    return await UserService(db).get_user_by_id(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def patch_user(
    user_id,
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    check_perm(current_user)

    updated_user = await AdminService(db).update_user(
        user_id, payload.model_dump(exclude_unset=True)
    )
    return updated_user


@router.delete(
    "/{user_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    user_id,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await AdminService(db).delete_user(user_id)


@router.post("/toggle-admin")
async def toggle_admin(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):

    current_user.role = (
        UserRole.ADMIN if current_user.role == UserRole.USER else UserRole.USER
    )
    await db.commit()
    await db.refresh(current_user)

    return {"new_role": f"{current_user.role}"}


def check_perm(current_user: User):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="insufficient permissions",
        )
