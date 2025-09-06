# 🧠 Bio AI Agent Infrastructure

> Идет отладка - 95% (tst, dev) - Next Up - DevOps Copilot

## disclaimer
> Basis [MVP], функционал дает создать чатик, создать проект с чатиками, сохранение истории (память пока в "сыром" виде), [загрузка ии-дрим-тим](https://github.com/justgithubaccount/app-release/blob/main/crewai-example.yaml) на базе CrewAI, подгрузка из Notion поведения (что то типо базовых паттернов)...  

> Это **AnyOps AI инженер** который будет следить за репой (этой) и девопсить проект и учиться на ошибках (инцеденты, логи, деплои...)...

> [Feature][модель психики для эмуляции сознания](https://github.com/justgithubaccount/psy-ooc-core), чтобы ии-агент (цифрофой двойник) развивался как живой организм за счет вылавливания "моментов взросления" (психоанализ + теория объектных отношений).  

> [Feature][био-пайплайны](https://github.com/justgithubaccount/bio-nextflow-blood) (пока пусто...) так как интересно направление биоинформатики (nextflow и прочие shakemake...). В ИИ-агенте будет включены био-пайплайны по анализу крови, рака и других био-операций...

##  tasks

### basis
- [x] [инфра] Настройить нджикc ингресс, серт менеджер, вэбки арго в паблик  
- [x] [инфра] Через external dns автомазировать работу с клаудфлейр по части днс | Манифестов добавить  
- [x] [инфра] Отладить хелм релиз для чат-апи | обернуть в апп-фор-аппс  
- [x] [код] отладить базовый функционал чата (пройти смок паблик тест) | стейт перенести в постгрее  
### sec
- [x] Добавить протект на майн-ветку | [проверить работу](https://github.com/justgithubaccount/app-release/actions/runs/16650220134/job/47120671590)
- [ ] ...  
### code
- [x] Убрать LiteLLM и сделать отдельный сервис, который будет напрямую ходить к OpenRouter
- [ ] Написать свой контролер | описываем схему через CRD | все в сути класс на го | все есть обьект | что сверху апишка, что снизу она же   
### infra 
- [ ] Отладить getting-started | сменить кластер  
- [ ] [запустить два+ кластера](https://github.com/justgithubaccount/app-release/blob/main/scripts/multi-cluster.yaml)  
- [ ] применить паттерн от Арго - ApplicationSet  
### ci
- [x] Добаваить тестов на предмет хелм рендеринда конфигов | добавить opa политики  
- [x] Добавить [семантическое версионирование](https://semver.org/lang/ru/) + git-теги + хелм-релиз-логика
  - [x] Добавить argocd-image-updater  
  - [ ] Тестить сборку релиза перед мерджем, в самом pr  
  - [x] сonventional сommits | всё в .releaserc.json | встроить флоу для гита  
### mesh
- [ ] Добавить сервис по анализу [инцидентов](https://github.com/justgithubaccount/app-release/issues/5)
- [ ] Продумать концепцию нейминга как под saas сервис
- [ ] Добавить прозрачность работы с env:
  - [x] ~~Интегрировать Consul~~ + external-secrets | консул не нужен | добавить плагин из экосистемы арго чтобы бегал в vault | external secret до облаков
  - [ ] Прикрутить service mesh. Линкерд или Истио | Линкерд у меня тут не 1kk RPS | консул был нужен как mesh, но лучше отдельный линкерд
  - [ ] Обеспечить возможность править env на лету (например, через SIGHUP или альтернативный механизм) | холиварный вопрос на счет таких подходов
  - [ ] Определить сервисы через Service + Endpoints [?]
  - [ ] [mesh] Создать отдельный сервис через cdktf, чтобы инфра сама себя воспроизводила (всм как бы добавить терраформа, но через питон) 

##  consept
> За счёт CrewAI и структурности это крайне универсальное решение, которое можно применить где угодно. Всё зависит от силы мысли и мечты.
>
> То, что в директории `context/` на первый взгляд кажется банальным — на самом деле просто слои памяти, контекста и наблюдений. Это не про «ответ нейронки», это про то, чтобы собрать своё понимание в код и вынести его в репу.
>
> Только мой мозг может сложить это в индивидуальную структуру и построить спираль. Это способ передать контекст — для тех, кто хочет не просто пользоваться, а узнать что-то новое.
>
> Лучше не следуй за мной по стопам, если боишься пустоты :)  

## getting started (clear install)
GitOps составляющая взята из подкаста [DKT66 - Что такое GitOps и с чего начать?](https://www.youtube.com/watch?v=5ljFkYqWN4c) + [репа так сказать к подкасту](https://github.com/devOwlish/argocd-demo) (в моем понимание ценности этой инфы нет предела)  

Логика ролевой системы для GitOps будет строится на моем прошлом опыте работы и архитектуры Active Directory (ну как ее строят в real-enterprise-shit)

---
Установить в новый кластер с нуля с восстановлением всех ресов кластера на основе роли (секреты нужно обновить)  
```bash
kubectl create namespace argocd  
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml  
git clone https://github.com/justgithubaccount/app-release.git  
cd app-release  
kubectl apply -f infra/_roles/role-dev-enviroment.yaml  
```
---
То что дальше требует обновления, но +/- так оно и есть, тесты, да нужно, накинуть...

## 📄 Содержание
- 🧠 [Архитектура классов chat-api](readme/chat-api-classes.md)
- ⚙️ [Использование OpenTelemetry](readme/open-telemetry.md)
- 🤖 [Определения CrewAI и поведение агентов](readme/crewai-definition.md)
- 📜 [Общий обзор CrewAI](readme/crewai-general.md)
- 🛠️ [Примеры задач для Codex](readme/codex-task-example.md)

Полный обзор микросервиса для работы с LLM (GPT-4 и др.), построенного на FastAPI, с CrewAI-интеграцией, observability-стеком, GitOps-деплоем и тестируемым CI/CD пайплайном.

---

## 📚 Описание проекта

Проект реализует микросервисную архитектуру, основной задачей которого является взаимодействие с LLM-моделью (через LiteLLM-прокси или напрямую). Внутри интеграция с Notion, CrewAI, observability через OpenTelemetry и инфраструктурная автоматизация.

---

## 🏗 Архитектура

### Основной микросервис: `chat-api`

* **FastAPI backend**: REST API (`/api/v1/chat`, `/health`, `/docs`, `/behavior/schema`)
* **Логика**: `services/chat_service.py`
* **LLM-клиент**: `core/llm_client.py`, использует LiteLLM / OpenAI API
* **Notion Behavior**: YAML-файл из Notion парсится в `BehaviorDefinition`
* **CrewAI YAML**: можно подключать Crew через YAML (см. `crew-infra-cluster.yaml`)

### Инфраструктура и DevOps:

* `ArgoCD` — GitOps-подход (слежение за `manifests/`)
* `SealedSecrets` — безопасное хранение API-ключей и конфигураций
* `LiteLLM` — деплой в отдельный pod (proxy над LLM)
* `Vector`, `Loki`, `Grafana` — observability стек
* `OpenTelemetry` + `structlog` — логгирование и трассировка

---

## 📂 Структура репозитория

```
apps/
  chat/
    app/          # Исходный код FastAPI приложения
      api.py
      main.py
      behavior/     # YAML-модели и схемы поведения
      core/         # Клиенты, конфиги, память
      models/       # Pydantic модели для истории чатов
      integrations/ # Notion client и behavior manager
      observability/
      services/
      schemas/
    crew-infra-cluster.yaml # YAML-определение Crew для CrewAI
    requirements.txt
manifests/
  ... # YAML манифесты для ArgoCD, ingress, sealed secrets
readme/
  open-telemetry.md
  codex-task-example.md
  chata-api-classes.md
scripts/
  context-chunk-export.sh
  k8s-basic.sh
  k8s-export-structured.sh
  ...
tests/
  behavior/test_models.py
  test_logging.py
Makefile
pyproject.toml
```

---

## 🚀 CI/CD и запуск

### GitHub Actions (`.github/workflows/build-and-push.yml`):

* Сборка Docker-образа `ghcr.io/justgithubaccount/chat-api:latest`
* Push в GitHub Container Registry

### ArgoCD:

* Автоматически следит за `manifests/chat-api-*.yaml`
* Применяет обновления и следит за дрейфом

---

## 🧪 Тестирование и запуск локально

### Установка зависимостей:

```bash
make dev  # установка dev-зависимостей
```

### Тесты:

```bash
make test  # pytest
```

### Локальный запуск:

```bash
make run   # запускает FastAPI
```

### Работа с БД и миграции

Используется SQLModel и PostgreSQL. URL подключения задаётся переменной `DATABASE_URL` (по умолчанию SQLite `sqlite:///db.sqlite3`).

Инициализация и миграции через Alembic:

```bash
alembic init alembic      # однократная инициализация
alembic revision --autogenerate -m "init"
alembic upgrade head
```

### Makefile (доступные команды):

```bash
make dev
make test
make lint
make fmt
make run
make docker
```

---

## 🔍 Observability и трассировка

* Логгирование: через `structlog`, enriched контекстом (trace\_id, span\_id)
* Трейсинг: через `OpenTelemetry + Loki`
* Метрики: Prometheus-compatible (`chat_requests_total` и др.)

```python
# enrich_context(event="chat_api_called", project_id=...) -> лог с trace_id
```

---

## 🧠 Интеграция с Notion и CrewAI

* YAML из Notion загружается при старте
* Преобразуется в `BehaviorDefinition` через `pydantic`
* Эндпоинт `/behavior/schema` возвращает текущее поведение

### YAML структура (Notion → Behavior):

```yaml
tasks:
  - description: "Search arXiv"
    expected_output: "Top 5 paper titles"
    context: ["Focus on GPT-4"]
    agent: "researcher"
agents:
  - role: "researcher"
    goal: "Understand GPT-4 applications"
    backstory: "PhD in ML"
    tools: ["browser"]
    allow_delegation: true
```

### Альтернативно: можно загрузить YAML через `Crew.load()`:

```python
from crewai import Crew
crew = Crew.load("crew-infra-cluster.yaml")
crew.kickoff()
```

---

## 📡 API маршруты

| Endpoint                        | Method   | Описание                             |
| ------------------------------- | -------- | ------------------------------------ |
| `/api/v1/chat`                  | POST     | Стандартный чат                      |
| `/api/v1/projects`              | GET/POST | Создание/список проектов             |
| `/api/v1/projects/{id}/chat`    | POST     | Чат внутри проекта (с историей)      |
| `/api/v1/projects/{id}/history` | GET      | История чата по trace\_id            |
| `/behavior/schema`              | GET      | Текущее поведение агента (из Notion) |
| `/health`                       | GET      | Healthcheck для k8s/Ingress          |

---

## 🔐 Безопасность

* `.env` → `SealedSecrets`
* Чувствительные ключи (`OPENAI_API_KEY`, `NOTION_TOKEN`) не коммитятся

```bash
kubeseal --format yaml < secret.yaml > chat-api-secrets-sealed.yaml
```

---

## 📌 Разделы в `readme/` (документация)

* `crewai-definition.md` — архитектура CrewAI и модели поведения
* `chata-api-classes.md` — описание всех классов микросервиса
* `open-telemetry.md` — observability и трассировка
* `codex-task-example.md` — как писать Codex-таски для автогенерации
* `source-v*.md` — версии исходников/архитектуры (исторические)

---

## 📈 Как масштабировать

* Добавить новые агенты/роли → в YAML в Notion или `crew-infra-cluster.yaml`
* Использовать MCP → логика `incident_llm_analyst`, `bioagent_mapper` и др.
* Подключить ClickHouse → для хранения больших объёмов логов и ответов

---

## 🧭 Заключение

Этот проект объединяет:

* Clean Architecture
* GitOps
* Observability
* CrewAI agent orchestration

Идеально подходит как стартер для AI-сервисов в production-среде.

> 🔁 Всё можно развёртывать и восстанавливать только по Git: infra as code, app as code, behavior as code.
