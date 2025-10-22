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
    "delete-unverified-users-daily-at-midnight": {
        "task": "delete_unverified_users",
        "schedule": crontab(
            hour=0, minute=0
        ),  # run every day at midnight delete unverified users for 2+ days
    },
}

celery.conf.timezone = "UTC"
