# Coffee Shop API - User Management Module

A production-ready FastAPI application implementing a complete user management system with authentication, authorization, email verification, and automated cleanup of unverified accounts.

## 🎯 Overview

This project is a user management microservice designed for a Coffee Shop API. It provides a robust, scalable foundation for handling user registration, authentication, role-based access control, and automated maintenance tasks.

## ✨ Features

### Authentication & Authorization

- **User Registration** - Email-based signup with optional name/surname
- **JWT Authentication** - Secure token-based authentication with access and refresh tokens
- **Email Verification** - Verification code sent via email (Resend API)
- **Role-Based Access Control** - Two roles: `User` and `Admin`
- **Token Refresh** - Seamless access token renewal

### User Management

- **Profile Access** - Users can view their own profile
- **Admin Dashboard** - Full CRUD operations for administrators
- **Partial Updates** - PATCH endpoint for flexible user data updates
- **Status Tracking** - PENDING and VERIFIED user statuses

### Automated Tasks

- **Cleanup Service** - Celery-based periodic task to automatically delete unverified users after 2 days
- **Scheduled Execution** - Uses Celery Beat for task scheduling

## 🏗️ Architecture

The project follows a clean, modular architecture with clear separation of concerns:

```
app/
├── auth/               # Authentication & authorization
│   ├── router.py      # Auth endpoints (signup, login, verify, refresh)
│   ├── schemas.py     # Pydantic models for request/response
│   ├── services.py    # Business logic for auth operations
│   └── utils.py       # Helper functions (cookies, email sending)
│
├── users/             # User management
│   ├── models.py      # SQLAlchemy User model
│   ├── router.py      # User CRUD endpoints
│   ├── schemas.py     # Pydantic models for users
│   ├── services.py    # User service layer
│   └── repository.py  # Database operations
│
├── config/            # Configuration & dependencies
│   ├── settings.py    # Environment configuration
│   ├── database.py    # Database connection setup
│   ├── jwt.py         # JWT token generation/validation
│   └── dependencies.py # FastAPI dependencies
│
├── tasks/             # Background tasks
│   ├── cleanup.py     # Cleanup unverified users task
│   └── __init__.py
│
├── core/              # Core utilities
│   └── enums.py       # Enums (UserStatus, UserRole)
│
├── celery.py          # Celery configuration
└── index.py           # FastAPI application entry point
```

### Key Design Patterns

- **Repository Pattern** - Data access abstraction
- **Service Layer** - Business logic separation
- **Dependency Injection** - Clean dependency management via FastAPI
- **Async/Await** - Fully asynchronous architecture for optimal performance

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.118+
- **Database**: PostgreSQL 16 with SQLAlchemy ORM
- **Task Queue**: Celery + Redis
- **Authentication**: JWT (python-jose)
- **Email Service**: Resend API
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest with pytest-asyncio
- **Migrations**: Alembic

## 📦 Prerequisites

- Docker & Docker Compose
- **Just** command runner (recommended for easier workflow)

### Installing Just

Just is a command runner that simplifies common development tasks.

**Linux:**

```bash
sudo snap install just --classic
```

**macOS:**

```bash
brew install just
```

**Other platforms:** Visit [just.systems](https://github.com/casey/just#installation)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/jamwujustyle/test_app.git
cd test_app
```

### 2. Configure Environment Variables

**⚠️ IMPORTANT:** You must add your Resend API key to the `.env` file.

1. Get your API key from [Resend](https://resend.com/api-keys)
2. Add it to your `.env` file:

```env
RESEND_API_KEY=your_resend_api_key_here
```

### 3. Set Up the Environment

```bash
just setup
```

This will configure necessary permissions and prepare the environment.

### 4. Start the Application

```bash
just start
```

This command will:

- Build Docker images
- Start all services (PostgreSQL, Redis, FastAPI, Celery Worker, Celery Beat)
- Run database migrations automatically
- Start the API server on `http://localhost:8002`

### 5. Access the API Documentation

Once running, visit:

- **Swagger UI**: http://localhost:8002/docs
- **ReDoc**: http://localhost:8002/redoc

**Note**: All API endpoints include comprehensive English summaries and descriptions in the OpenAPI documentation. Each endpoint clearly explains its purpose, required permissions, and expected behavior.

## 📝 Available Just Commands

The `justfile` provides convenient shortcuts for common operations:

| Command        | Description                                |
| -------------- | ------------------------------------------ |
| `just start`   | Build and start all services               |
| `just stop`    | Stop all running services                  |
| `just down`    | Stop and remove all containers and volumes |
| `just setup`   | Run initial setup script                   |
| `just migrate` | Generate and apply database migrations     |
| `just test`    | Run the test suite                         |

### Examples

```bash
# Start the application
just start

# Run migrations after model changes
just migrate

# Run tests
just test

# Stop everything
just stop

# Complete cleanup (removes volumes)
just down
```

## 🔐 API Endpoints

### Authentication

| Method | Endpoint        | Description            | Access |
| ------ | --------------- | ---------------------- | ------ |
| POST   | `/auth/signup`  | Register a new user    | Public |
| POST   | `/auth/login`   | Login with credentials | Public |
| POST   | `/auth/verify`  | Verify email with code | Public |
| POST   | `/auth/refresh` | Refresh access token   | Public |

### User Management

| Method | Endpoint      | Description              | Access        |
| ------ | ------------- | ------------------------ | ------------- |
| GET    | `/users/me`   | Get current user profile | Authenticated |
| GET    | `/users/`     | List all users           | Admin only    |
| GET    | `/users/{id}` | Get user by ID           | Admin only    |
| PATCH  | `/users/{id}` | Update user (partial)    | Admin only    |
| DELETE | `/users/{id}` | Delete user              | Admin only    |

### Example API Usage

#### 1. Register a New User

```bash
curl -X POST "http://localhost:8002/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "name": "John",
    "surname": "Doe"
  }'
```

#### 2. Verify Email

Check your email for the verification code, then:

```bash
curl -X POST "http://localhost:8002/auth/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "code": "123456"
  }'
```

#### 3. Login

```bash
curl -X POST "http://localhost:8002/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

## 🧪 Testing

The project includes comprehensive test coverage for critical functionality.

### Running Tests

```bash
# Using Just
just test

# Or directly with Docker
docker exec -it test_app bash -c "pytest -v --disable-warnings"
```

### Test Structure

```
tests/
├── conftest.py              # Test fixtures and configuration
├── test_cleanup_task.py     # Cleanup task tests
└── README.md                # Testing documentation
```

## 🔄 Background Tasks

### Cleanup Task

The application includes an automated Celery task that runs daily at midnight to clean up unverified user accounts.

**Configuration:**

- **Task Name**: `delete_unverified_users`
- **Schedule**: Daily at 00:00 UTC (using crontab)
- **Function**: Deletes users with status `PENDING` who have been in that status for 2+ days

**Implementation Details:**

```python
# Located in: app/celery.py
celery.conf.beat_schedule = {
    "delete-unverified-users-daily-at-midnight": {
        "task": "delete_unverified_users",
        "schedule": crontab(hour=0, minute=0),  # Run daily at midnight
    },
}
```

**⚠️ Implementation Note:**

The original task description specified: _"Users who have not been verified within 2 days should be automatically deleted."_

To implement this correctly, I added a `created_at` timestamp field to the User model. This field was not explicitly mentioned in the original requirements but was necessary to:

1. **Track user age**: Determine which users have been in PENDING status for 2+ days
2. **Precise deletion**: Only delete users created 2+ days ago, not all unverified users on every run
3. **Prevent premature deletion**: Avoid deleting newly registered users who are still within their 2-day verification window

**Why this change was necessary:**

Without the `created_at` field, the cleanup task would have deleted ALL pending users every time it ran, including users who had just registered minutes ago. The `created_at` timestamp ensures that only users who have exceeded the 2-day grace period are removed.

**Database Schema Addition:**

```python
# app/users/models.py
created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False
)
```

This deviation improves the robustness and correctness of the cleanup mechanism while maintaining the spirit of the original requirement.

### Monitoring Celery Tasks

To view task execution logs:

```bash
# Worker logs
docker logs test_worker -f

# Beat scheduler logs
docker logs test_beat -f
```

## 🐳 Docker Services

The application uses the following containerized services:

| Service   | Port | Description                      |
| --------- | ---- | -------------------------------- |
| `app`     | 8002 | FastAPI application              |
| `test_db` | 5433 | PostgreSQL database              |
| `redis`   | 6379 | Redis (Celery broker/backend)    |
| `worker`  | -    | Celery worker for task execution |
| `beat`    | -    | Celery Beat for task scheduling  |
| `migrate` | -    | Runs migrations on startup       |

## 📊 Database Schema

### User Model

```python
- id: UUID (Primary Key)
- email: String (Unique, Indexed)
- password: String (Hashed)
- name: String (Optional)
- surname: String (Optional)
- role: Enum (USER, ADMIN)
- status: Enum (PENDING, VERIFIED)
- created_at: DateTime
```

## 🔧 Configuration

Key environment variables (defined in `.env`):

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=test_db
DATABASE_URL=postgresql+asyncpg://postgres:postgres@test_db:5432/test_db

# JWT
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Resend API (REQUIRED)
RESEND_API_KEY=your_resend_api_key_here

# Redis
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

## 🛡️ Security Features

- **Password Hashing** - Passwords are hashed using bcrypt
- **JWT Tokens** - Short-lived access tokens (30 minutes) + long-lived refresh tokens (7 days) (Multiplied for convenience)
- **HTTP-Only Cookies** - Tokens stored in secure HTTP-only cookies
- **Role-Based Access** - Endpoint protection based on user roles
- **Email Verification** - Required before account activation
