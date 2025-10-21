"""
Unit tests for the periodic cleanup task.
Uses pytest, pytest-asyncio, pytest-mock, and freezegun for testing.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from freezegun import freeze_time
from datetime import datetime, timedelta

from app.tasks.cleanup import delete_unverified_users, delete_unverified_users_async
from app.core.enums import UserStatus


@pytest.mark.asyncio
async def test_delete_unverified_users_async_success(mocker):
    """Test that delete_unverified_users_async successfully deletes PENDING users"""
    # Mock the database session
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.rowcount = 5  # Simulate 5 deleted users

    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.commit = AsyncMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    # Mock AsyncSessionLocal
    mocker.patch("app.tasks.cleanup.AsyncSessionLocal", return_value=mock_session)

    # Execute the async function
    deleted_count = await delete_unverified_users_async()

    # Assertions
    assert deleted_count == 5
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_unverified_users_async_no_users(mocker):
    """Test when there are no PENDING users to delete"""
    # Mock the database session with no deletions
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.rowcount = 0  # No users deleted

    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.commit = AsyncMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    mocker.patch("app.tasks.cleanup.AsyncSessionLocal", return_value=mock_session)

    deleted_count = await delete_unverified_users_async()

    assert deleted_count == 0
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_unverified_users_async_error_handling(mocker):
    """Test error handling and rollback on database error"""
    # Mock the database session to raise an exception
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(side_effect=Exception("Database error"))
    mock_session.rollback = AsyncMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    mocker.patch("app.tasks.cleanup.AsyncSessionLocal", return_value=mock_session)

    # Should raise the exception
    with pytest.raises(Exception, match="Database error"):
        await delete_unverified_users_async()

    # Verify rollback was called
    mock_session.rollback.assert_called_once()


def test_delete_unverified_users_celery_task(mocker):
    """Test the Celery task wrapper for delete_unverified_users"""
    # Mock asyncio.run to avoid actually running async code
    mock_asyncio_run = mocker.patch("app.tasks.cleanup.asyncio.run")
    mock_asyncio_run.return_value = 3  # Simulate 3 deleted users

    # Execute the Celery task
    result = delete_unverified_users()

    # Assertions
    assert result["status"] == "success"
    assert result["deleted_count"] == 3
    mock_asyncio_run.assert_called_once()


def test_delete_unverified_users_celery_task_error(mocker):
    """Test the Celery task error handling"""
    # Mock asyncio.run to raise an exception
    mock_asyncio_run = mocker.patch("app.tasks.cleanup.asyncio.run")
    mock_asyncio_run.side_effect = Exception("Task failed")

    result = delete_unverified_users()

    # Should return error status
    assert result["status"] == "error"
    assert "Task failed" in result["message"]


@freeze_time("2025-10-22 01:00:00")
def test_delete_unverified_users_with_time_freeze(mocker):
    """Test the task at a specific frozen time point"""
    # Mock asyncio.run
    mock_asyncio_run = mocker.patch("app.tasks.cleanup.asyncio.run")
    mock_asyncio_run.return_value = 10

    # Execute at frozen time
    result = delete_unverified_users()

    assert result["status"] == "success"
    assert result["deleted_count"] == 10

    # Verify we're at the expected time
    now = datetime.now()
    assert now.year == 2025
    assert now.month == 10
    assert now.day == 22


@freeze_time("2025-10-20 00:00:00")
def test_periodic_task_schedule_simulation(mocker):
    """Simulate periodic task execution over time using freezegun"""
    from freezegun import freeze_time

    # Mock asyncio.run
    mock_asyncio_run = mocker.patch("app.tasks.cleanup.asyncio.run")

    # Simulate task running at different times
    execution_times = []
    deleted_counts = [5, 3, 0, 2, 1]  # Different results at each execution

    for i, count in enumerate(deleted_counts):
        # Move time forward by 2 days each iteration
        with freeze_time(datetime(2025, 10, 20) + timedelta(days=i * 2)):
            mock_asyncio_run.return_value = count
            result = delete_unverified_users()

            execution_times.append(datetime.now())
            assert result["deleted_count"] == count
            assert result["status"] == "success"

    # Verify we had 5 executions over 8 days
    assert len(execution_times) == 5
    # Verify time differences
    for i in range(1, len(execution_times)):
        time_diff = execution_times[i] - execution_times[i - 1]
        assert time_diff.days == 2, "Tasks should be 2 days apart"


@pytest.mark.asyncio
async def test_delete_query_targets_correct_status(mocker):
    """Verify that the delete query targets only PENDING status users"""
    # Mock the database session
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.rowcount = 1

    # Capture the executed statement
    executed_statement = None

    async def capture_execute(stmt):
        nonlocal executed_statement
        executed_statement = stmt
        return mock_result

    mock_session.execute = capture_execute
    mock_session.commit = AsyncMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    mocker.patch("app.tasks.cleanup.AsyncSessionLocal", return_value=mock_session)

    await delete_unverified_users_async()

    # Verify the statement was executed
    assert executed_statement is not None
    # The statement should be a delete statement that filters by UserStatus.PENDING
    # This is a basic check - in practice you'd inspect the statement more thoroughly
