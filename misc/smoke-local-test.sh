#!/bin/bash

set -e

echo "🔍 1. Проверка /health у litellm:"
curl -s -o /dev/null -w "litellm health: %{http_code}\n" http://localhost:4000/health

echo "🔍 2. Проверка OpenAPI JSON у chat-api:"
curl -s -o /dev/null -w "openapi.json: %{http_code}\n" http://localhost:8000/openapi.json

echo "🔍 3. Проверка /docs у chat-api:"
curl -s -o /dev/null -w "docs: %{http_code}\n" http://localhost:8000/docs

echo "🧠 4. Проверка chat/completions у litellm:"
RESPONSE=$(curl -s -X POST http://localhost:4000/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "openai/gpt-4.1",
    "messages": [
      {"role": "system", "content": "Ты ассистент, отвечай лаконично."},
      {"role": "user", "content": "Привет! Скажи как дела?"}
    ]
  }')
echo "Ответ от litellm:"
echo "$RESPONSE"
echo

echo "💬 5. Проверка chat-api (старый endpoint /chat):"
RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [
      {"role": "user", "content": "Как дела?"}
    ]
  }')
echo "Ответ от chat-api:"
echo "$RESPONSE"
echo

echo "📁 6. Создание проекта:"
PROJECT=$(curl -s -X POST http://localhost:8000/api/v1/projects \
  -H 'Content-Type: application/json' \
  -d '{"name": "Test Project"}')
PROJECT_ID=$(echo $PROJECT | grep -oP '"id":\s*"\K[^"]+')
echo "Создан проект с ID: $PROJECT_ID"
echo

echo "💬 7. Отправка сообщения в рамках проекта:"
RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/projects/$PROJECT_ID/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [
      {"role": "user", "content": "Расскажи анекдот"}
    ]
  }')
echo "Ответ от chat-api в проекте:"
echo "$RESPONSE"
echo

echo "📜 8. Получение истории проекта:"
RESPONSE=$(curl -s http://localhost:8000/api/v1/projects/$PROJECT_ID/history)
echo "История сообщений:"
echo "$RESPONSE"
echo

echo "✅ Все проверки завершены."
