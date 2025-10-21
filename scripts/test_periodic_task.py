#!/usr/bin/env python3
"""
Script to manually trigger the periodic cleanup task for testing purposes.
This allows you to test the delete_unverified_users task without waiting 2 days.
"""
import sys
import os

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.celery import celery


def test_delete_unverified_users():
    """Manually trigger the delete_unverified_users task"""
    print("Triggering delete_unverified_users task...")

    # Send the task to Celery worker
    result = celery.send_task("delete_unverified_users")

    print(f"Task sent! Task ID: {result.id}")
    print("Waiting for result...")

    # Wait for the task to complete and get the result
    try:
        task_result = result.get(timeout=10)
        print(f"\nTask completed successfully!")
        print(f"Result: {task_result}")
    except Exception as e:
        print(f"\nError executing task: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(test_delete_unverified_users())
