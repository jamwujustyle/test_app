from pydantic import BaseModel, Field, ConfigDict

from typing import Optional, List
from uuid import UUID

from app.core import UserRole, UserStatus


class UserResponse(BaseModel):

    id: UUID
    # TODO: RM LATER

    email: str = Field(..., description="Unique email address of the user.")
    name: Optional[str] = Field(
        None, description="First name of the user, if provided."
    )
    surname: Optional[str] = Field(
        None, description="Last name of the user, if provided."
    )
    status: str = Field(
        ...,
        description="Account status indicating whether the user is verified or pending verification.",
    )
    role: str = Field(
        ..., description="Role assigned to the user, e.g., 'admin' or 'user'."
    )

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    users: List[UserResponse]


class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    status: Optional[UserStatus] = None
    role: Optional[UserRole] = None
