from celery import Celery
from celery.schedules import crontab

from app.users.models import User


celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.tasks"],
)

celery.autodiscover_tasks(["app.tasks"])

# Configure Celery Beat schedule
celery.conf.beat_schedule = {
    "delete-unverified-users-every-2-days": {
        "task": "delete_unverified_users",
        "schedule": 172800.0,  # 2 days in seconds (2 * 24 * 60 * 60)
    },
}

celery.conf.timezone = "UTC"
