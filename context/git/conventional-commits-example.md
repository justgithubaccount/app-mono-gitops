**Conventional Commits структура:**

```
<тип>(<область>): <описание>

[тело коммита]

[футер]
```

## **Основные типы:**

**🚀 MINOR (новые функции)**
```bash
feat: добавить API endpoint для получения истории чатов
feat(api): интеграция с OpenTelemetry трейсингом  
feat(k8s): добавить HorizontalPodAutoscaler
feat(helm): поддержка multi-environment деплоя
```

**🐛 PATCH (исправления)**
```bash
fix: исправить ошибку валидации в chat endpoint
fix(api): правильная обработка пустых сообщений
fix(helm): добавить отсутствующий RBAC для ServiceAccount
fix(db): исправить миграцию схемы PostgreSQL
```

**💥 MAJOR (breaking changes)**
```bash
feat!: изменить формат API ответа на REST v2
fix!: удалить deprecated endpoints /api/v1/old
feat(api)!: изменить схему базы данных чатов
```

## **Области (scope) для твоего проекта:**

- `api` - FastAPI endpoints
- `chat` - логика чат сервиса
- `llm` - интеграция с LLM провайдерами
- `db` - изменения базы данных
- `k8s` - Kubernetes манифесты
- `helm` - Helm chart изменения
- `ci` - GitHub Actions workflows
- `observability` - метрики, логи, трейсинг
- `docker` - Dockerfile изменения
- `crewai` - агенты и crew конфигурация

## **Примеры для твоих задач:**

**Приложение:**
```bash
feat(chat): добавить streaming responses для real-time чата
fix(llm): исправить timeout при обращении к OpenAI API
feat(api): добавить health check endpoint с detailed status
```

**DevOps/Infrastructure:**
```bash
feat(k8s): добавить ArgoCD sync waves для правильного порядка деплоя
fix(helm): исправить RBAC permissions для chat-api ServiceAccount
feat(ci): автоматическая упаковка Helm chart в GitHub release
```

**Observability:**
```bash
feat(observability): добавить OpenTelemetry spans для всех API вызовов
fix(tracing): правильно экспортировать spans в Jaeger
feat(metrics): добавить Prometheus метрики для LLM запросов
```

**Breaking Changes:**
```bash
feat(api)!: изменить структуру chat message schema

BREAKING CHANGE: поле 'content' переименовано в 'message_content'
Для миграции замените все вызовы API с новой схемой
```

**Сводка по работе на уровне системы:**
- **Commit Parser:** `@semantic-release/commit-analyzer` читает тип → определяет bump
- **Version Calculation:** feat→minor, fix→patch, !→major  
- **Changelog Generation:** scope группирует изменения по компонентам
- **GitOps Integration:** Каждый коммит → GitHub API → ArgoCD → K8s API
- **Traceability:** OpenTelemetry трейсит от коммита до деплоя