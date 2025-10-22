from celery import shared_task
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from datetime import datetime, timedelta

from app.users.models import User
from app.core.enums import UserStatus
from app.config.database import AsyncSessionLocal


async def delete_unverified_users_async():
    """Delete users with PENDING status who have been pending for 2+ days"""
    async with AsyncSessionLocal() as session:
        try:
            # Calculate the cutoff time (2 days ago)
            cutoff_time = datetime.now() - timedelta(days=2)

            # Delete users with PENDING status created more than 2 days ago
            stmt = delete(User).where(
                User.status == UserStatus.PENDING, User.created_at <= cutoff_time
            )
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
    Celery task to delete users who have been in PENDING status for 2+ days.
    This task runs periodically to clean up old unverified users.
    """
    try:
        deleted_count = asyncio.run(delete_unverified_users_async())
        print(
            f"Successfully deleted {deleted_count} unverified users (pending for 2+ days)"
        )
        return {"status": "success", "deleted_count": deleted_count}
    except Exception as e:
        print(f"Error deleting unverified users: {str(e)}")
        return {"status": "error", "message": str(e)}
