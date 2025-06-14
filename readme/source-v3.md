Вот расширенное **техдосье** по текущему состоянию проекта — включая последние изменения, задачи Codex-агента и новую архитектуру поведения через YAML и Notion.

---

# 🧠 **AI Chat Microservice — расширенный контекст (v2)**

## 🔧 Назначение
Микросервис `chat-api` оборачивает LLM-провайдеров в REST API (`/api/v1/chat`), позволяет настраивать поведение агентов (LLM) через YAML и Notion, и теперь подключает CrewAI-компоненты (agents, tasks, crews) декларативно.

## 📁 Структура

```
apps/chat/
├── app/
│   ├── main.py                  # FastAPI точка входа
│   ├── api.py                   # Chat endpoint
│   ├── behavior/                # Pydantic-модели для поведения
│   ├── integrations/
│   │   ├── behavior_manager.py  # YAML/Notion → поведение
│   │   ├── notion_client.py
│   ├── services/chat_service.py # ядро общения с LLM
│   ├── core/                    # config, health, memory
│   ├── observability/          # tracing
│   ├── logger.py
│   ├── crew-infra-cluster.yaml # описание Crew (CrewAI)
│   └── tests/                  # pytest-тесты
```

## ⚙️ YAML-архитектура

Ты используешь YAML-файл `crew-infra-cluster.yaml` с описанием `Crew`, включающего:

- `roles`: агенты (инфра, ArgoCD, LLM, BioOps и т.д.)
- `goal`, `tools`, `memory`, `context`, `example` — поведенческая модель
- Используется в `main.py`:

```python
from crewai import Crew
crew = Crew.load('crew-infra-cluster.yaml')
crew.kickoff()
```

Это инициализирует Crew из YAML при запуске FastAPI, делая поведение декларативным и версионируемым.

## 🧠 Notion-режим

Через `BehaviorManager` реализована загрузка поведения из Notion (по `NOTION_PAGE_ID`) в виде YAML.

```python
yaml_str = notion_client.download_yaml()
parsed = BehaviorDefinition.parse_raw(yaml_str)
```

Модель `BehaviorDefinition` описывает поля схемы:

```python
TaskSchema
  ↳ description
  ↳ expected_output
  ↳ tags

AgentSchema
  ↳ role, goal, backstory, tools
```

## 🔬 Codex: Автоматизация по коду

Codex-агент уже получил задачу:

> Найти все endpoints, сервисы, обработчики, классы Pydantic, и описать их как Agent/Task схемы.

Он работает с локальными исходниками и Notion одновременно. Генерирует `crew`-схему либо напрямую (на уровне файла), либо отправляет Pull Request.

## ✅ CI + Make

Добавлен `Makefile` для локального запуска:

```make
test:
	pytest -q --tb=short --disable-warnings

lint:
	ruff apps/chat/app

run:
	uvicorn apps.chat.app.main:app --reload
```

CI запускается через GitHub Actions (`.github/workflows/build-and-push.yml`) и билдит образ:

```yaml
- uses: docker/build-push-action@v5
  with:
    context: ./apps/chat
    tags: ghcr.io/justgithubaccount/chat-api:latest
```

---

## 🧪 Test-редим
Pytest с моделями уже работает:

```bash
pytest tests/behavior/test_models.py
```

Если окружение ломается, ошибка чаще всего:

- `ModuleNotFoundError: No module named 'app'` — решается через `PYTHONPATH=.` или правильный layout в `pyproject.toml`.

---

## 🧠 Поведение Agenta как структура

Всё поведение (и в Notion, и в crewai.yaml) — это **настраиваемый, сериализуемый "мозг" агента**, описанный:

- Через `goal`, `context`, `tools`, `memory`
- Через `example` (few-shot learning)
- Через YAML или Markdown в Notion

Это позволяет:

- Обновлять поведение агента без изменений кода
- Версионировать его в git
- Делать его наблюдаемым и описываемым

---

## 🧩 Задача Codex для автогенерации поведения

Codex получил:

```yaml
task:
  description: >
    Сгенерируй Task-и и Agent-описания на основе всех handler'ов FastAPI,
    включая описание цели, моделей, примеров.
  expected_output: >
    Обновлённый behavior.yaml (или Markdown для Notion) + Pull Request.
  context: >
    Проект использует FastAPI, все endpoints в /app/api.py и app/services.
    Требуется описать каждую бизнес-логику как Task.
```

---

Если надо, можно отдать это всё как единый ZIP / README другим разработчикам, либо сделать export Notion → YAML → Git через Codex.

Хочешь экспорт шаблона или генерацию AgentBuilder?