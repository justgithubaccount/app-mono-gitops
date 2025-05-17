# Chat Microservice

FastAPI-based LLM chat microservice.

## Запуск (локально)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Запуск в Docker
docker compose down -v && docker compose build --no-cache && docker compose up