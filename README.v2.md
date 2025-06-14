Спасибо, теперь понял: **кластер уже перенесён**, и тебе нужен полный, связный контекст по проекту, который можно отдать как "досье" — чтобы было понятно, как всё работает, как устроено и какие компоненты есть. Без фокуса на миграцию, а с упором на описание и диагностику.

Вот такой **полный контекст** (Markdown-ready):

---

# 🧩 **Полный контекст по проекту: AI Chat Microservice**

> Этот документ описывает архитектуру, назначение, структуру, пайплайн CI/CD, используемые технологии и стандартные команды для диагностики и эксплуатации.

---

## 📚 **1. Назначение проекта**

**AI Chat Microservice** — это облачный микросервис для чата с LLM (GPT-4 и другие модели), развёрнутый в Kubernetes-кластере.
Архитектура построена по принципу GitOps (ArgoCD), полностью автоматизирована, поддерживает безопасное хранение секретов (SealedSecrets), вертикальное и горизонтальное масштабирование, а также быструю замену компонентов.

---

## ⚙️ **2. Архитектура и компоненты**

### Основные сервисы:

* **FastAPI chat-api** — основной микросервис для общения с LLM (REST API: `/api/v1/chat`).
  Поддерживает health-check (`/health`), документацию (`/docs`), конфигурируется через env/secrets.
* **LiteLLM** — прокси для LLM-провайдеров (OpenAI, OpenRouter и др.).
  Вынесен в отдельный деплоймент, управляет токенами через Secret, конфиг через ConfigMap.
* **Nginx Ingress** — маршрутизация публичных HTTP(S) запросов (с DNS, например, `chat.syncjob.ru`).
* **ArgoCD** — автоматическая синхронизация состояния кластера с репозиторием GitHub.
* **SealedSecrets** — безопасное хранение всех секретных переменных (API-ключи, токены) прямо в git.

### Инфраструктурные моменты:

* Namespace: обычно всё в `chat-api`, кроме ingress-nginx и argocd.
* Все деплои и сервисы описаны декларативно в yaml-файлах (`manifests/`).

---

## 🗂 **3. Структура репозитория**

```
.
├── README.md
├── apps
│   └── chat               # FastAPI-приложение
│       ├── Dockerfile
│       ├── app            # исходники python
│       └── requirements.txt
├── manifests
│   ├── chat-api-application.yaml     # ArgoCD Application
│   ├── chat-api-deployment.yaml      # FastAPI Deployment
│   ├── chat-api-service.yaml         # FastAPI Service
│   ├── chat-api-ingress.yaml         # Ingress
│   ├── chat-api-secrets-sealed.yaml  # SealedSecret (API-ключи)
│   ├── litellm-configmap.yaml        # ConfigMap для LiteLLM
│   ├── litellm-deployment.yaml       # LiteLLM Deployment
│   ├── litellm-service.yaml          # LiteLLM Service
│   ├── litellm-secrets-sealed.yaml   # SealedSecret для LiteLLM
├── .github
│   └── workflows
│       └── build-and-push.yml        # CI для Docker
```

---

## 🚀 **4. CI/CD и GitOps**

* **GitHub Actions**:

  * Каждый пуш в `main` → сборка docker-образа (`chat-api`) и пуш в GitHub Container Registry.
  * Сборка берёт исходники из `apps/chat`.
  * Используются теги: `ghcr.io/justgithubaccount/chat-api:latest`
* **ArgoCD**:

  * Следит за состоянием манифестов в `manifests/`.
  * При изменении манифеста (или выходе нового образа) — автоматически пересоздаёт деплойменты.
* **Kubernetes**:

  * Развёртывание только из git: руками в кластере ничего не меняется (devops-best-practice).

---

## 🔐 **5. Безопасность и секреты**

* Все переменные (ключи API, токены и т.д.) лежат в `SealedSecret` и дешифруются только в k8s-кластере.
* Обычные секреты генерируются через `kubeseal`.
* Чувствительные файлы типа `.env` — не в git.

---

## 🌐 **6. Внешние адреса и маршрутизация**

* Для публичного доступа используется DNS (например, `chat.syncjob.ru`).
* В ingress yaml прописан host, путь `/` прокидывает на сервис chat-api (FastAPI, порт 8000 через сервис 80).
* LiteLLM доступен только изнутри кластера (ClusterIP, port 4000).

---

## 💡 **7. Основные команды и диагностика**

### Проверка деплоя:

```bash
kubectl get pods -n chat-api
kubectl get svc -n chat-api
kubectl get ingress -n chat-api
kubectl logs -n chat-api -l app=chat-api | tail -n 50
kubectl logs -n chat-api -l app=litellm | tail -n 50
```

### Проверка работы API:

```bash
curl http://chat.syncjob.ru/
curl http://chat.syncjob.ru/docs
curl -s -X POST "http://chat.syncjob.ru/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "Ты ассистент, отвечай лаконично."},
      {"role": "user", "content": "Привет! Как дела?"}
    ]
  }'
```

### Проверка ingress-контроллера:

```bash
kubectl get svc -n ingress-nginx
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx | tail -n 100
```

---

## 🏗 **8. Важные принципы эксплуатации**

* Все изменения только через Git → CI → ArgoCD (никаких ручных `kubectl apply`).
* Для новых секретов всегда использовать SealedSecret.
* В случае изменений переменных окружения или конфига — просто коммит в git и Argo всё подтянет.
* Для управления поведением агента через Notion задайте `NOTION_TOKEN` и `NOTION_PAGE_ID` в переменных окружения.
* Для отладки — использовать логи pod-ов, а не "залезание внутрь".

---

## 🎯 **9. Как расширять**

* Добавлять новые микросервисы — копируя паттерн chat-api (deployment, service, ingress, secret).
* Для тестовых запусков — делать отдельный namespace и ветку.
* Интеграция с мониторингом/логированием (Prometheus, Grafana, Loki) — через отдельные manifests.

---

## 📝 **10. Диагностика типовых проблем**

* **502/404 от ingress:** проверь правильность host и endpoints, убедись что сервисы поднимаются (`kubectl get endpoints -n chat-api`).
* **500 от FastAPI:** смотри логи приложения и Litellm.
* **403/401 от LiteLLM:** смотри правильность API-ключа и поддерживаемые модели.
* **Арго не пересоздаёт деплой:** проверь webhooks и актуальность manifests/ в репозитории.

---

## 📌 **Вывод**

Текущий проект полностью описан декларативно (infra-as-code, app-as-code, secrets-as-code), поддерживает быструю миграцию, замену LLM-провайдера, масштабирование и работу в проде/стейдже.

**Для передачи в команду или новую локацию:**

* Достаточно дать этот README, файлы manifests/ и инструкции по SealedSecret.
* Всё остальное подтянет CI/CD и ArgoCD.

---

**Если нужен sample-код, примеры манифестов, CI/CD pipeline или пояснения — просто пиши!**

---
