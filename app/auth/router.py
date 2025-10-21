from fastapi.routing import APIRouter
from fastapi import Depends, Response, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from .utils import set_auth_cookies
from .services import refresh_access_token

from app.users.services import UserService
from app.core import UserStatus
from app.config import get_db, create_refresh_token, create_access_token


router = APIRouter(prefix="auth")


@router.post("/signup", response_model=RegisterResponse)
async def register(
    request: RegisterRequest, db: AsyncSession = Depends(get_db)
) -> bool:
    try:
        await UserService(db).create_user(
            email=request.email,
            password=request.password,
            name=request.name,
            surname=request.surname,
        )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="already registered or invalid",
        )
    return RegisterResponse(verified=False)


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)
):
    user = await UserService(db).authenticate_user(
        email=request.email, password=request.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid email or pass"
        )

    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="activate ur account"
        )

    tokens = {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }
    set_auth_cookies(response, tokens)

    return LoginResponse(success=True, message="login successful")


@router.post("/refresh")
async def refresh(
    response: Response, request: Request, result: dict = Depends(refresh_access_token)
):
    return result
