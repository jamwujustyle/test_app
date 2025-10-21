start:
    docker compose up --build

stop:
    docker compose down

down:
    docker compose down -v


setup:
    chmod +x ./scripts/set-env && ./scripts/set-env


migrate:
    docker exec -it test_app bash -c "alembic revision --autogenerate -m 'auto' && alembic upgrade head"

test:
    docker exec -it test_app bash -c "pytest -v --disable-warnings"

