#!/bin/bash

set -e

echo "1. Проверка /health у litellm:"
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4000/health

echo "2. Проверка OpenAPI JSON:"
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/openapi.json

echo "3. Проверка chat/completions на litellm (openai/gpt-4o):"
RESPONSE=$(curl -s -X POST http://localhost:4000/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "openai/gpt-4.1",
    "messages": [
      {"role": "system", "content": "Ты ассистент, отвечай лаконично."},
      {"role": "user", "content": "Привет! Скажи как дела?"}
    ]
  }')
echo "$RESPONSE"

echo "4. Проверка chat-сервиса через его docs (если FastAPI):"
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/docs

echo "Все проверки завершены."
