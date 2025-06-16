#!/bin/bash
set -e

### ============================
### 🌐 Public endpoint
### ============================
BASE_CHAT_API="http://chat.syncjob.ru"

### 1. Check /health on litellm
echo "🔍 [1] Checking /health on litellm"
curl --fail -s -o /dev/null -w "litellm health: %{http_code}\n" "$BASE_CHAT_API/health"

### 2. Check OpenAPI docs
echo "🔍 [2] Checking OpenAPI JSON"
curl --fail -s -o /dev/null -w "openapi.json: %{http_code}\n" "$BASE_CHAT_API/openapi.json"

### 3. Check /docs page
echo "🔍 [3] Checking /docs UI"
curl --fail -s -o /dev/null -w "docs: %{http_code}\n" "$BASE_CHAT_API/docs"

### 4. POST /chat/completions (litellm logic)
echo "🧠 [4] Checking litellm: /chat/completions"
RESPONSE=$(curl -s -X POST "$BASE_CHAT_API/chat/completions" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "openai/gpt-4.1",
    "messages": [
      {"role": "system", "content": "Ты ассистент, отвечай лаконично."},
      {"role": "user", "content": "Привет! Скажи как дела?"}
    ]
  }')
echo "🔁 litellm response:"
echo "$RESPONSE"
echo

### 5. Old /chat endpoint (chat-api legacy)
echo "💬 [5] Checking chat-api legacy endpoint"
RESPONSE=$(curl -s -X POST "$BASE_CHAT_API/api/v1/chat" \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [
      {"role": "user", "content": "Как дела?"}
    ]
  }')
echo "🔁 chat-api legacy response:"
echo "$RESPONSE"
echo

### 6. Create project
echo "📁 [6] Creating new project"
PROJECT=$(curl -s -X POST "$BASE_CHAT_API/api/v1/projects" \
  -H 'Content-Type: application/json' \
  -d '{"name": "Test Project"}')
PROJECT_ID=$(echo $PROJECT | grep -oP '"id":\s*"\K[^"]+')
echo "✅ Project created: $PROJECT_ID"
echo

### 7. Send message inside the project
echo "💬 [7] Sending message to project chat"
RESPONSE=$(curl -s -X POST "$BASE_CHAT_API/api/v1/projects/$PROJECT_ID/chat" \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [
      {"role": "user", "content": "Расскажи анекдот"}
    ]
  }')
echo "🔁 chat-api project response:"
echo "$RESPONSE"
echo

### 8. Retrieve message history
echo "📜 [8] Fetching project history"
RESPONSE=$(curl -s "$BASE_CHAT_API/api/v1/projects/$PROJECT_ID/history")
echo "📄 Message history:"
echo "$RESPONSE"
echo

echo "✅ Public smoke test completed successfully."
