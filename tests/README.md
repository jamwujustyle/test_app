# Testing the Periodic Cleanup Task

This document explains how to test the periodic cleanup task that runs every 2 days without having to wait.

## Testing Tools

The project uses the following testing libraries (from `requirements.txt`):

- **pytest**: Test framework
- **pytest-asyncio**: Support for async/await tests
- **pytest-mock**: Mocking framework
- **freezegun**: Time manipulation for testing time-dependent behavior

## Quick Start

Run all tests:

```bash
pytest
```

Run only the cleanup task tests:

```bash
pytest tests/test_cleanup_task.py
```

Run with verbose output:

```bash
pytest -v tests/test_cleanup_task.py
```

## Test Coverage

The test suite (`tests/test_cleanup_task.py`) includes:

### 1. Unit Tests with Mocking

- `test_delete_unverified_users_async_success` - Tests successful deletion of pending users
- `test_delete_unverified_users_async_no_users` - Tests when no users need deletion
- `test_delete_unverified_users_async_error_handling` - Tests error handling and rollback
- `test_delete_unverified_users_celery_task` - Tests the Celery task wrapper
- `test_delete_unverified_users_celery_task_error` - Tests Celery task error handling

### 2. Time-Based Tests with Freezegun

- `test_delete_unverified_users_with_time_freeze` - Tests execution at a specific frozen time
- `test_periodic_task_schedule_simulation` - Simulates the task running over multiple days

### 3. Query Verification

- `test_delete_query_targets_correct_status` - Verifies the correct SQL query is executed

## Testing Approaches

### Approach 1: Unit Tests (Recommended for CI/CD)

Run the automated test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app.tasks --cov-report=html

# Run specific test
pytest tests/test_cleanup_task.py::test_delete_unverified_users_async_success -v
```

**Advantages:**

- Fast execution (milliseconds)
- No dependencies on external services
- Perfect for CI/CD pipelines
- Uses freezegun to simulate time passage
- Comprehensive coverage of edge cases

### Approach 2: Manual Task Trigger

Use the provided script to manually trigger the task:

```bash
# Make sure Celery worker is running first
python scripts/test_periodic_task.py
```

**Requirements:**

- Redis must be running
- Celery worker must be running
- Database must be accessible

**Advantages:**

- Tests the actual task execution
- Tests integration with Celery and Redis
- Verifies database operations

### Approach 3: Temporary Schedule Modification

Temporarily change the schedule to run more frequently:

1. Open `app/celery.py`
2. Replace the schedule value:

   ```python
   # From (2 days):
   "schedule": 172800.0,

   # To (30 seconds):
   "schedule": 30.0,
   ```

3. Restart Celery Beat worker
4. Observe logs for task execution every 30 seconds
5. **Remember to revert the change after testing!**

**Reference configurations are provided in `app/celery_test_config.py`**

### Approach 4: Time Manipulation with Freezegun (Automated in Tests)

The test suite already uses freezegun to test periodic behavior. See:

```python
@freeze_time("2025-10-20 00:00:00")
def test_periodic_task_schedule_simulation(mocker):
    """Simulates task running over multiple 2-day periods"""
    # This test simulates 5 executions over 8 days
    # without actually waiting
```

## Running the Application Stack

If you need to test with the full stack running:

```bash
# Start all services (PostgreSQL, Redis, Celery, etc.)
docker-compose up -d

# View Celery worker logs
docker-compose logs -f celery_worker

# View Celery Beat logs
docker-compose logs -f celery_beat

# Stop all services
docker-compose down
```

## Test Database Setup

For integration testing with a real database:

1. Create a test database configuration
2. Run migrations: `alembic upgrade head`
3. Seed test data with PENDING users
4. Run the manual trigger script or wait for scheduled execution
5. Verify users were deleted

## Continuous Integration

Add to your CI pipeline:

```yaml
# Example for GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest tests/ -v --cov=app.tasks
```

## Troubleshooting

### Tests fail with import errors

```bash
# Ensure you're in the project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

### Celery worker not picking up tasks

```bash
# Restart Celery worker
docker-compose restart celery_worker

# Check worker is connected to Redis
redis-cli ping
```

### Database connection issues in tests

The tests mock the database by default, so they don't need a real database connection.

## Best Practices

1. **Always run unit tests first** - They're fast and catch most issues
2. **Use freezegun for time-based tests** - Don't actually wait for time to pass
3. **Mock external dependencies** - Database, Redis, etc. in unit tests
4. **Use integration tests sparingly** - Only when you need to verify full stack behavior
5. **Clean up after tests** - Remove any test data created during integration tests

## Example Test Run

```bash
$ pytest tests/test_cleanup_task.py -v

tests/test_cleanup_task.py::test_delete_unverified_users_async_success PASSED
tests/test_cleanup_task.py::test_delete_unverified_users_async_no_users PASSED
tests/test_cleanup_task.py::test_delete_unverified_users_async_error_handling PASSED
tests/test_cleanup_task.py::test_delete_unverified_users_celery_task PASSED
tests/test_cleanup_task.py::test_delete_unverified_users_celery_task_error PASSED
tests/test_cleanup_task.py::test_delete_unverified_users_with_time_freeze PASSED
tests/test_cleanup_task.py::test_periodic_task_schedule_simulation PASSED
tests/test_cleanup_task.py::test_delete_query_targets_correct_status PASSED

========== 8 passed in 0.42s ==========
```

All tests pass in under a second, and they simulate the behavior of the 2-day periodic task!
