"""
Pytest configuration and fixtures for testing.
"""

import pytest


@pytest.fixture
def mock_celery_task(mocker):
    """Fixture to mock Celery task execution"""
    return mocker.patch("app.tasks.cleanup.delete_unverified_users")


@pytest.fixture
def mock_async_session(mocker):
    """Fixture to mock AsyncSessionLocal"""
    mock_session = mocker.AsyncMock()
    mock_session.__aenter__ = mocker.AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = mocker.AsyncMock(return_value=None)
    return mock_session
