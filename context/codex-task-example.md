Вот подробное **техническое задание (ТЗ)** для senior Python-разработчика (или ИИ Codex), чтобы он реализовал систему тестирования и CI по best practices, ориентированную на продакшен и Cloud Native подходы:

---

## 🧩 Техническое задание: Настройка тестов и CI для FastAPI-сервиса

### 🎯 Цель:

Обеспечить полное покрытие тестами и интеграцию тестов в CI/CD pipeline на GitHub Actions для FastAPI-приложения (`apps/chat/app`), включая unit, integration и API schema tests. Всё должно соответствовать best practices, быть production-ready и совместимо с cloud-native подходами (CNCF-friendly).

---

### 📦 Входные данные:

* Python >= 3.10
* Приложение FastAPI внутри `apps/chat/app`
* Текущая структура: `apps/chat/app/{api.py, main.py, behavior/, integrations/, core/}`
* Есть `pyproject.toml`, `docker-compose.yml`, `.github/workflows/`
* Есть LLM-интеграция (`CrewAI`), OpenTelemetry, `notion-client`, `structlog`
* В `tests/` есть зачатки: `test_models.py`, `test_logging.py`

---

### 📌 Задачи:

1. **Покрытие кода тестами**

   * Написать unit-тесты для:

     * `BehaviorDefinition`, `AgentSchema`, `TaskSchema`
     * `notion_client.py` (моки и HTTP-заглушки)
     * `llm_client`, `chat_service`
   * Написать integration-тесты:

     * для `/behavior/schema` (FastAPI TestClient)
     * подключение crewai и yaml-файлов
   * Примеры: `tests/behavior/test_models.py`, `tests/integrations/test_endpoints.py`

2. **Тестовый фреймворк**

   * Использовать `pytest` как основной фреймворк
   * Настроить `conftest.py` с фикстурами
   * Добавить `pytest.ini` или `pyproject.toml` конфиг с testpaths

3. **Линтеры и типы**

   * Интеграция `ruff` и `mypy` через Makefile
   * Обработка `PYTHONPATH`, или использование `editable install` (`-e .`) для `apps/chat/app`

4. **Makefile**

   * Добавить команды:

     ```make
     test: pytest
     lint: ruff .
     type: mypy apps/chat/app
     check: lint type test
     ci: check
     ```

5. **CI/CD**

   * Добавить `.github/workflows/test.yaml`

     ```yaml
     on:
       push:
         branches: [main]
     jobs:
       test:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v3
           - uses: actions/setup-python@v4
             with:
               python-version: "3.10"
           - name: Install deps
             run: |
               python -m pip install --upgrade pip
               pip install -e .[dev]
           - name: Run tests
             run: make ci
     ```

6. **Pyproject/requirements**

   * Обновить `pyproject.toml`:

     ```toml
     [project.optional-dependencies]
     dev = ["pytest", "mypy", "ruff", "httpx", "coverage"]
     ```
   * Либо создать `requirements-dev.txt`

---

### ✅ Результат:

* Все тесты успешно выполняются через `make test`
* Покрытие критичных компонентов ≥ 80%
* GitHub Actions прогоняет тесты и линтеры
* Тесты легко запускаются локально и в контейнере
* Приложение соответствует стандартам FastAPI/pyproject/ruff

---

Если нужно — могу сразу сгенерировать шаблон `Makefile`, `test_endpoints.py`, `ci.yaml`. Скажи только, хочешь ли ты видеть это сейчас.
