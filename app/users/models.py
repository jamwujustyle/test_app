from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, DateTime
from sqlalchemy.sql import func

from passlib.context import CryptContext

from app.config.database import Base
from app.core import UserStatus, UserRole

from uuid import UUID, uuid4
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
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
    # NOTE: I would've had these fields in a separate table in a larger application
    verification_code: Mapped[str] = mapped_column(String(6), nullable=True)
    verification_code_expires: Mapped[datetime] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def generate_verification_code(self) -> str:
        import random

        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        self.verification_code = code
        self.verification_code_expires = datetime.now() + timedelta(minutes=15)
        return code

    def verify_code(self, code: str) -> bool:
        if not self.verification_code or not self.verification_code_expires:
            return False

        if datetime.now() > self.verification_code_expires:
            return False

        return self.verification_code == code

    def set_password(self, plain_password: str) -> None:
        self.password = pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)
