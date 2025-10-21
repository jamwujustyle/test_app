from celery import Celery

from app.users.models import User


celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.tasks"],
)

celery.autodiscover_tasks("app.tasks")
