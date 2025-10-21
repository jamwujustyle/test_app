from fastapi.routing import APIRouter
from fastapi import Depends, Response, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    VerifyRequest,
)
from .utils import set_auth_cookies, send_verification_email
from .services import refresh_access_token

from app.users.services import UserService
from app.core import UserStatus
from app.config import get_db, create_refresh_token, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=RegisterResponse,
    summary="Register a new user",
    description="Create a new user account with email and password. After registration, a verification code will be sent to the provided email address. The user will have PENDING status until email verification is completed.",
)
async def register(
    request: RegisterRequest, db: AsyncSession = Depends(get_db)
) -> bool:
    try:
        _, code = await UserService(db).create_user_with_verification(
            email=request.email,
            password=request.password,
            name=request.name,
            surname=request.surname,
        )

        await send_verification_email(email=request.email, code=code)

        return RegisterResponse(
            verified=False, message=f"Verification code sent to {request.email}"
        )

    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"already registered or invalid: {str(ex)}",
        )


@router.post(
    "/verify",
    response_model=RegisterResponse,
    summary="Verify email address",
    description="Verify user's email address using the verification code sent during registration. Upon successful verification, the user status changes to VERIFIED and authentication tokens are issued.",
)
async def verify(
    request: VerifyRequest, response: Response, db: AsyncSession = Depends(get_db)
):
    user = await UserService(db).verify_user_email(
        email=request.email, code=request.code
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code",
        )

    tokens = {
        "access_token": create_access_token(user_id=user.id, email=user.email),
        "refresh_token": create_refresh_token(user.id),
    }
    set_auth_cookies(response, tokens)

    return RegisterResponse(verified=True, message="Email verified successfully")


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="User login",
    description="Authenticate user with email and password credentials. Returns access and refresh tokens stored in HTTP-only cookies. User must have VERIFIED status to successfully login.",
)
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

    if user.status != UserStatus.VERIFIED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="activate ur account"
        )

    tokens = {
        "access_token": create_access_token(user_id=user.id, email=user.email),
        "refresh_token": create_refresh_token(user.id),
    }
    set_auth_cookies(response, tokens)

    return LoginResponse(success=True, message="login successful")


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Generate a new access token using the refresh token stored in cookies. This endpoint allows users to maintain their session without re-authenticating.",
)
async def refresh(
    response: Response, request: Request, result: dict = Depends(refresh_access_token)
):
    return result
