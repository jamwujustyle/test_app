from fastapi import Request, Response, HTTPException, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from ..config import (
    get_db,
    verify_refresh_token,
    create_access_token,
    create_refresh_token,
)
from ..users.repository import UserRepo

from .utils import set_auth_cookies

import uuid


async def refresh_access_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):

    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
        )

    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user_repo = UserRepo(db)
    user = await user_repo.get_by_id(uuid.UUID(user_id_str))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    new_access_token = create_access_token(user.id, user.email)
    new_refresh_token = create_refresh_token(user.id)

    tokens = {"access_token": new_access_token, "refresh_token": new_refresh_token}

    set_auth_cookies(response, tokens)

    return {"message": "Tokens refreshed successfully"}
