Вот **архитектура проекта observability-ready FastAPI микросервиса**, в духе Cloud Native и GitOps:

---

## 🧩 **Архитектура по слоям**

### 1️⃣ **API Layer (FastAPI endpoints)**

* Обрабатывает входящие HTTP-запросы.
* Использует `ChatRequest` / `ChatResponse` (из `schemas.py`) для валидации и генерации OpenAPI.
* Пример: `/chat` endpoint.

### 2️⃣ **Observability Layer**

✅ **OpenTelemetry SDK**

* Генерирует трейсы (Trace → Spans).
* Позволяет связать метрики, логи и запрос.

✅ **Structlog + Processors**

* Конфигурирован с `add_trace_context`, который добавляет в лог:

  * `trace_id`
  * `span_id`
  * `timestamp`, `event`, `endpoint`, `project_id`

✅ **Metrics (OpenTelemetry Counter)**

* `chat_requests_total` — считает входящие запросы по тегу `project_id`.

---

### 3️⃣ **Data Models Layer**

#### `schemas.py`

📤 Схемы для API I/O:

* Чистые `Pydantic`-модели, с `alias`, `example`, и без trace-мета.

#### `models.py`

📦 Схемы для хранения:

* `StoredChatMessage`, включает:

  * `timestamp`
  * `trace_id`, `span_id`
  * `project_id`, `message`, `role`, `id`

Можно писать напрямую в:

* ✅ ClickHouse (через логи)
* ✅ S3 (архив)
* 📝 PostgreSQL (если нужно)

---

### 4️⃣ **Log Storage Layer (Grafana Stack-ready)**

* **Loki** — собирает JSON-логи через Promtail или Vector.
* **Grafana** — отображает логи с фильтрацией по `trace_id`, `project_id`.

---

### 5️⃣ **Tracing Layer (Tempo/Jaeger)**

* Каждый запрос создаёт трейсы через OpenTelemetry.
* Возможность отследить путь запроса → метрика → лог.
* Связь по `trace_id`, `span_id`.

---

### 6️⃣ **Metrics Layer (Prometheus/Grafana)**

* Через `OpenTelemetry Metrics SDK`.
* Метрики `chat_requests_total`, future: latency, error\_rate.
* Можно экспортировать в Prometheus через OTLP Collector.

---

## 🔗 **Пример потока данных запроса**

```
POST /chat
  └── validate ChatRequest
      └── enrich_context (event=chat_request)
          └── span создан (OpenTelemetry)
              ├── лог с trace_id
              ├── chat_counter.add(...)
              └── reply → ChatResponse
                  └── лог хранения StoredChatMessage
```

---

## 📁 Cloud Native Ready

| Компонент      | Готовность                       |
| -------------- | -------------------------------- |
| GitOps         | ✅ (всё описывается декларативно) |
| Observability  | ✅ Logs + Metrics + Traces        |
| OpenAPI        | ✅ schemas → Swagger UI           |
| Слои разделены | ✅ API / Models / Storage / Logs  |
| ClickHouse     | ✅ Логи пригодны для ingestion    |
| S3 Архив       | ✅ `StoredChatMessage` совместим  |

---

Хочешь — добавим:

* экспорт логов в S3/ClickHouse,
* ingestion через Vector,
* авто-добавление user-agent, request-id и др.

Готов собрать `.drawio` или `.png`-схему по слоям — если нужно визуально.
