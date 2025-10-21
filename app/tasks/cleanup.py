from celery import shared_task
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

from app.users.models import User
from app.core.enums import UserStatus
from app.config.database import AsyncSessionLocal


async def delete_unverified_users_async():
    """Delete all users with PENDING status"""
    async with AsyncSessionLocal() as session:
        try:
            # Delete users with PENDING status
            stmt = delete(User).where(User.status == UserStatus.PENDING)
            result = await session.execute(stmt)
            await session.commit()

            deleted_count = result.rowcount
            return deleted_count
        except Exception as e:
            await session.rollback()
            raise e


@shared_task(name="delete_unverified_users")
def delete_unverified_users():
    """
    Celery task to delete users who are not verified (status = PENDING).
    This task is scheduled to run every 2 days.
    """
    try:
        deleted_count = asyncio.run(delete_unverified_users_async())
        print(f"Successfully deleted {deleted_count} unverified users")
        return {"status": "success", "deleted_count": deleted_count}
    except Exception as e:
        print(f"Error deleting unverified users: {str(e)}")
        return {"status": "error", "message": str(e)}
