from pydantic import BaseModel, Field, ConfigDict

from typing import Optional


class UserResponse(BaseModel):
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
