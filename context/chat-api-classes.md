Вот полное описание архитектуры классов текущего проекта `AI Chat Microservice`, структурированное по слоям:

---

# 🧱 Архитектура классов AI Chat Microservice

Проект построен на FastAPI, структурирован по слоям (core, services, schemas, models, integrations), расширен поддержкой поведения агентов (CrewAI-style) через Notion.

---

## 📁 `app/main.py`

**Точка входа** — создаёт FastAPI-приложение, подключает:

* роутеры (`api_router`, `health_router`),
* CORS,
* OpenTelemetry-трейсинг (`setup_tracing`),
* поведение агентов из Notion через `BehaviorManager`.

---

## 🧠 Слой: `behavior`

### `BehaviorDefinition`

```python
class BehaviorDefinition(BaseModel):
    agents: List[AgentSchema]
    tasks: List[TaskSchema]
    process: Optional[str]
```

* Описывает YAML-структуру поведения агентов (роль, цель, инструменты, делегирование, задачи).

### `AgentSchema`

* Агент в стиле CrewAI: `role`, `goal`, `backstory`, `tools`, `tasks`.

### `TaskSchema`

* Описание задачи, которую агент должен выполнить (описание, результат, контекст, агент).

---

## 🧩 Слой: `schemas`

### `Message`, `ChatRequest`, `ChatResponse`

* Pydantic-схемы, определяющие формат общения с LLM.

### `ProjectInfo`, `CreateProjectRequest`

* Схемы проектов (ID, имя), поддерживают проекты с историей диалогов.

---

## 💾 Слой: `models`

### `StoredChatMessage`, `ChatHistory`

* Хранилище истории диалогов в памяти: кто сказал, что, когда, trace\_id/span\_id.

---

## 🛠 Слой: `services`

### `ChatService`

* Основная бизнес-логика:

  * вызывает LLM (`OpenRouterClient`),
  * логирует события (через `enrich_context`),
  * оборачивает ошибки и выводит метки (`job=chat`, `trace_id`).

---

## 🧬 Слой: `core`

### `OpenRouterClient`

* Асинхронный HTTP-клиент (httpx), вызывает `/chat/completions` на LiteLLM/LLM API.
* Поддерживает `project_id`, `user_api_key`, `trace_id`.

### `ProjectMemory`

* Временное хранилище проектов и их истории в оперативке.

### `health.py`

* `/health` endpoint для Kubernetes.

### `config.py`

* `Settings` на основе `.env`: токены, URL LLM, модель, project\_name.

---

## 🧩 Слой: `integrations`

### `NotionClient`

* Обёртка над API Notion, получает YAML-данные о поведении агентов.

### `BehaviorManager`

* Загружает YAML из Notion → парсит в `BehaviorDefinition`.
* Доступен как `app.state.behavior_manager`.

---

## 📜 API

### `/api/v1/chat`

* Обработка сообщений пользователя → вызов LLM → возврат ответа.

### `/api/v1/projects`

* Создание и просмотр проектов.

### `/api/v1/projects/{id}/chat`

* Отправка сообщений в рамках проекта.

### `/behavior/schema`

* Отдаёт текущую схему поведения из Notion.

---

## 🧪 Тесты

Тесты (WIP):

* `tests/behavior/test_models.py` — проверка схем `BehaviorDefinition`.
* `tests/test_logging.py` — проверка enrich\_context и логов.

---

## 📦 Возможные расширения

* ✅ Добавление Crew YAML через `Crew.load(...)`
* ✅ Интеграция с Vector/Loki через job-теги
* 🔄 Возможность импорта behavior напрямую в Crew (при наличии crewai CLI в окружении)

---

Если тебе нужно:

* Генерация диаграммы классов
* Ссылки между API endpoints и классами
* Полный OpenAPI spec + JSON schemas

— просто скажи, и я сгенерирую.
