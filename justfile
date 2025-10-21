start:
    docker compose up --build

stop:
    docker compose down

down:
    docker compose down -v


setup:
    chmod +x ./scripts/set-env && ./scripts/set-env