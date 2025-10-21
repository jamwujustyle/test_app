"""
Celery configuration for TESTING purposes only.
This configuration changes the periodic task schedule to run every 30 seconds
instead of every 2 days, allowing you to test the periodic behavior quickly.

USAGE:
1. Stop your current Celery Beat worker
2. Temporarily modify app/celery.py to use this schedule
3. Start Celery Beat again
4. Observe the task running every 30 seconds
5. Remember to revert to the original schedule after testing!
"""

from celery.schedules import crontab

# TEST SCHEDULE - Runs every 30 seconds
TEST_BEAT_SCHEDULE = {
    "delete-unverified-users-every-30-seconds": {
        "task": "delete_unverified_users",
        "schedule": 30.0,  # 30 seconds for testing
    },
}

# TEST SCHEDULE - Runs every 1 minute
TEST_BEAT_SCHEDULE_1MIN = {
    "delete-unverified-users-every-1-minute": {
        "task": "delete_unverified_users",
        "schedule": 60.0,  # 1 minute for testing
    },
}

# PRODUCTION SCHEDULE - Runs every 2 days
PRODUCTION_BEAT_SCHEDULE = {
    "delete-unverified-users-every-2-days": {
        "task": "delete_unverified_users",
        "schedule": 172800.0,  # 2 days in seconds (2 * 24 * 60 * 60)
    },
}
