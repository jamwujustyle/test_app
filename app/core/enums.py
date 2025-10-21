from enum import StrEnum


class base(StrEnum):
    @classmethod
    def choices(cls):
        return [(tag.value, tag.name.capitalize()) for tag in cls]


class UserStatus(base):
    PENDING = "pending"
    VERIFIED = "verified"


class UserRole(base):
    USER = "user"
    ADMIN = "admin"
