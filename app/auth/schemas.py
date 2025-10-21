from pydantic import Field, BaseModel, EmailStr

from typing import Optional


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="user's email, must be unique")
    password: str = Field(..., description="user's password")
    name: Optional[str] = Field(None, description="username, optional")
    surname: Optional[str] = Field(None, description="user's surname, optional")


class RegisterResponse(BaseModel):
    verified: bool


class LoginRequest(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)


class LoginResponse(BaseModel):
    success: bool
    message: str


class ResendCodeRequest(BaseModel):
    email: EmailStr = Field(...)


class VerifyRequest(BaseModel):
    email: EmailStr = Field(...)
    code: str = Field(..., min_length=6, max_length=6)
