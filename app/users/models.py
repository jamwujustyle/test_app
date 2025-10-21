from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum

from app.config.database import Base
from app.core import UserStatus, UserRole


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), nullabe=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    name: Mapped[str] = mapped_column(String(100))
    surname: Mapped[str] = mapped_column(String(100))

    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=UserStatus.PENDING,
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, values_callable=lambda x: [e.value for e in x]),
        nullable=True,
        default=UserRole.USER,
    )
