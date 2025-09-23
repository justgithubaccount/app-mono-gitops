# 🏢 Multi-tenant ML + Application архитектура в ArgoCD

## 🧠 Архитектурная проблема

**В компании есть:**
- **ML Team**: тренирует модели, деплоит inference сервисы
- **App Team**: разрабатывает приложения, которые используют эти модели
- **DevOps Team**: управляет инфраструктурой

**Нужны отдельные среды:**
- ML-платформа (GPU кластеры, model registry, MLflow)
- App-платформа (обычные приложения, API, фронтенд)
- Разные права доступа для разных команд

---

## 🏗️ Расширенная RBAC-схема через `_main_apps`

### Текущая схема (по кластерам):
```
_main_apps/
├── prd.yaml    # Production кластер
└── dev.yaml    # Development кластер
```

### Новая схема (по командам + кластерам):
```
_main_apps/
├── ml-prd.yaml      # ML команда → Production ML кластер
├── ml-dev.yaml      # ML команда → Development ML кластер  
├── app-prd.yaml     # App команда → Production App кластер
├── app-dev.yaml     # App команда → Development App кластер
├── platform-prd.yaml   # DevOps → Production infrastructure
└── platform-dev.yaml   # DevOps → Development infrastructure
```

---

## 🔐 RBAC Mapping

| Команда | Права в Git | ArgoCD Application | Целевой кластер |
|---------|-------------|-------------------|------------------|
| **ML Team** | `ml-*` branches, `/ml/**` paths | `ml-prd.yaml`, `ml-dev.yaml` | GPU clusters |
| **App Team** | `app-*` branches, `/app/**` paths | `app-prd.yaml`, `app-dev.yaml` | App clusters |
| **DevOps** | `main` branch, `/platform/**` paths | `platform-*.yaml` | All clusters |
| **Security** | Review-only | - | Audit access |

---

## 📁 Структура репозитория

```
infra/
├── _main_apps/                    # RBAC: кто куда может
│   ├── ml-prd.yaml               # ML → ML Production
│   ├── ml-dev.yaml               # ML → ML Development  
│   ├── app-prd.yaml              # App → App Production
│   ├── app-dev.yaml              # App → App Development
│   ├── platform-prd.yaml        # DevOps → Platform
│   └── platform-dev.yaml        # DevOps → Platform
├── clusters/                      # Environment configs
│   ├── ml-prd/                   # ML Production cluster config
│   ├── ml-dev/                   # ML Development cluster config
│   ├── app-prd/                  # App Production cluster config
│   ├── app-dev/                  # App Development cluster config
│   ├── platform-prd/             # Platform Production
│   └── platform-dev/             # Platform Development
├── base/
│   ├── ml/                       # ML платформа
│   │   ├── kubeflow/            # ML orchestration
│   │   ├── mlflow/              # Model registry
│   │   ├── jupyter/             # Notebooks
│   │   ├── model-serving/       # Inference services
│   │   └── gpu-operator/        # GPU management
│   ├── app/                      # Application платформа
│   │   ├── chat-api/            # Твое chat приложение
│   │   ├── frontend/            # Frontend apps
│   │   ├── api-gateway/         # API management
│   │   └── databases/           # App databases
│   └── platform/                # Shared infrastructure
│       ├── ingress-nginx/       # Load balancing
│       ├── cert-manager/        # TLS certificates
│       ├── monitoring/          # Observability
│       └── security/            # Policies, RBAC
```

---

## 🎯 Конкретные манифесты

### ML Team RBAC
```yaml
# _main_apps/ml-prd.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ml-production
  namespace: argocd
  labels:
    team: ml
    environment: production
spec:
  project: ml-project              # ArgoCD Project для ML команды
  destination:
    name: ml-prd-cluster          # GPU кластер для ML
    namespace: argocd
  source:
    repoURL: https://github.com/company/ml-platform.git
    path: clusters/ml-prd
    targetRevision: main
  syncPolicy:
    automated:
      selfHeal: true
      prune: true
    syncOptions:
      - CreateNamespace=true
```

```yaml
# clusters/ml-prd/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namePrefix: ml-prd-
namespace: ml-production

resources:
  # ML-специфичные компоненты
  - ../../../base/ml/kubeflow
  - ../../../base/ml/mlflow  
  - ../../../base/ml/model-serving
  - ../../../base/ml/gpu-operator
  
  # Общая платформа (только необходимое)
  - ../../../base/platform/monitoring
  - ../../../base/platform/security

patches:
  - target:
      kind: Application
    patch: |-
      - op: replace
        path: /spec/destination/name  
        value: ml-prd-cluster
```

### App Team RBAC
```yaml
# _main_apps/app-prd.yaml
apiVersion: argoproj.io/v1alpha1  
kind: Application
metadata:
  name: app-production
  namespace: argocd
  labels:
    team: app
    environment: production
spec:
  project: app-project              # ArgoCD Project для App команды
  destination:
    name: app-prd-cluster          # Обычный кластер для приложений
    namespace: argocd
  source:
    repoURL: https://github.com/company/app-platform.git
    path: clusters/app-prd
    targetRevision: main
  syncPolicy:
    automated:
      selfHeal: true
      prune: true
```

```yaml
# clusters/app-prd/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namePrefix: app-prd-
namespace: app-production

resources:
  # App-специфичные компоненты
  - ../../../base/app/chat-api
  - ../../../base/app/frontend
  - ../../../base/app/api-gateway
  - ../../../base/app/databases
  
  # Общая платформа
  - ../../../base/platform/ingress-nginx
  - ../../../base/platform/cert-manager
  - ../../../base/platform/monitoring

patches:
  - target:
      kind: Application  
    patch: |-
      - op: replace
        path: /spec/destination/name
        value: app-prd-cluster
```

---

## 🔗 Интеграция ML + App

### Model Serving для App команды
```yaml
# base/ml/model-serving/inference-service.yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: chat-model-v1
  namespace: ml-production
spec:
  predictor:
    pytorch:
      storageUri: "s3://ml-models/chat-model/v1"
      resources:
        requests:
          nvidia.com/gpu: 1
        limits:
          nvidia.com/gpu: 1
---
# Service для App команды
apiVersion: v1
kind: Service
metadata:
  name: chat-model-api
  namespace: ml-production
  annotations:
    external-dns.alpha.kubernetes.io/hostname: chat-model.internal.company.com
spec:
  selector:
    app: chat-model-v1-predictor
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
```

### App использует модель
```yaml
# base/app/chat-api/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chat-api
spec:
  template:
    spec:
      containers:
      - name: chat-api
        image: company/chat-api:latest
        env:
        - name: ML_MODEL_ENDPOINT
          value: "http://chat-model.internal.company.com"
        - name: MODEL_VERSION
          value: "v1"
```

---

## 🛡️ Git-based RBAC

### Branch Protection Rules
```yaml
# .github/branch-protection.yml
branches:
  main:
    required_reviews: 2
    required_reviewers: ["devops-team"]
    restrict_pushes: true
    
  ml-*:
    required_reviews: 1  
    required_reviewers: ["ml-team-leads"]
    paths: ["ml/**", "_main_apps/ml-*.yaml"]
    
  app-*:
    required_reviews: 1
    required_reviewers: ["app-team-leads"] 
    paths: ["app/**", "_main_apps/app-*.yaml"]
```

### ArgoCD Projects (дополнительная изоляция)
```yaml
# argocd-projects/ml-project.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: ml-project
  namespace: argocd
spec:
  description: ML Team Project
  
  # Разрешенные source repos
  sourceRepos:
  - 'https://github.com/company/ml-platform.git'
  - 'https://github.com/company/ml-models.git'
  
  # Разрешенные destination clusters
  destinations:
  - namespace: 'ml-*'
    server: 'https://ml-prd-cluster.company.com'
  - namespace: 'ml-*'  
    server: 'https://ml-dev-cluster.company.com'
    
  # Разрешенные Kubernetes ресурсы
  namespaceResourceWhitelist:
  - group: ''
    kind: Secret
  - group: 'apps'
    kind: Deployment
  - group: 'serving.kserve.io'
    kind: InferenceService
  - group: 'kubeflow.org'
    kind: Notebook
    
  clusterResourceWhitelist:
  - group: 'nvidia.com'
    kind: '*'  # GPU resources
```

---

## 🔄 Workflow Example

### ML Team деплоит новую модель:
```bash
# 1. ML engineer делает PR в ml-dev ветку
git checkout -b ml-dev/new-chat-model
git add clusters/ml-dev/models/chat-model-v2.yaml
git commit -m "Deploy chat model v2 to ML dev"
git push origin ml-dev/new-chat-model

# 2. ArgoCD автоматически подхватывает изменения
# только в ML dev кластере (благодаря _main_apps/ml-dev.yaml)

# 3. После тестирования - PR в main
git checkout main
git merge ml-dev/new-chat-model  # С review от ML team lead

# 4. ArgoCD деплоит в ML production
```

### App Team использует новую модель:
```bash
# 1. App engineer обновляет конфиг приложения
git checkout -b app-dev/use-model-v2
# Меняет MODEL_VERSION на v2 в app configs
git commit -m "Switch to chat model v2"

# 2. Деплой в app dev environment для тестирования
# 3. После тестирования - PR в main для production
```

---

## 🎯 Преимущества этой схемы

### 1. **Изоляция команд**
- ML команда не может сломать App production
- App команда не имеет доступа к GPU ресурсам
- DevOps контролирует платформенные компоненты

### 2. **Гибкость развертывания**  
- ML может деплоить модели независимо
- App может использовать модели через стабильный API
- Версионирование моделей и приложений отдельно

### 3. **Безопасность**
- Git-based RBAC + ArgoCD Projects
- Namespace isolation  
- Resource quotas per team

### 4. **Observability**
- Отдельный мониторинг для ML (GPU метрики, model performance)
- Отдельный мониторинг для App (business метрики)
- Unified платформенный мониторинг

---

## 🚀 Migration Plan

### Phase 1: Структура
1. Создать новые `_main_apps` файлы для команд
2. Разделить `clusters/` по командам  
3. Настроить ArgoCD Projects

### Phase 2: ML Platform
1. Деплой Kubeflow в ML кластеры
2. Настройка model registry (MLflow)
3. Model serving infrastructure

### Phase 3: Integration
1. Настройка service discovery между кластерами
2. API gateway для доступа к моделям
3. Мониторинг и алертинг

### Phase 4: Team Onboarding
1. Обучение команд новым процессам
2. Настройка Git permissions
3. Production deployment

---

Отличный вопрос! 🎯 Ты говоришь про **multi-tenant архитектуру** где нужно разделить **ML-платформу** и **Application-платформу**. Это классическая задача для крупных компаний. Покажу как это элегантно решить в твоей RBAC-схеме.## 🎯 Как это работает на практике

**Твоя RBAC-схема идеально подходит для multi-tenant!** Вместо разделения только по environment (dev/prd), добавляем разделение по **командам + environment**.

### 🔑 Ключевая идея:
- **`_main_apps/ml-prd.yaml`** = "ML команда может деплоить в ML production кластер"
- **`_main_apps/app-prd.yaml`** = "App команда может деплоить в App production кластер"  
- **`clusters/ml-prd/`** = "Что разрешено в ML production" (GPU, Kubeflow, MLflow)
- **`clusters/app-prd/`** = "Что разрешено в App production" (chat-api, frontend, databases)

### 🔗 Интеграция ML → App:
1. **ML команда** деплоит модель в ML кластер → создается inference endpoint
2. **App команда** использует этот endpoint через service discovery или API gateway
3. **DevOps** управляет networking между кластерами

### 🛡️ Безопасность:
- Git branch protection: ML команда может коммитить только в `ml/**` пути
- ArgoCD Projects: дополнительная изоляция ресурсов
- Kubernetes RBAC: namespace isolation внутри кластеров

## 📊 Сводка по системе:

**Обращение к Kubernetes API:** Каждая команда имеет свой ArgoCD Application → свой набор permissions → свой кластер/namespace

**Принцип зон ответственности:**
- **ML Zone**: GPU кластеры, model training/serving, ML tools
- **App Zone**: Business applications, databases, frontend  
- **Platform Zone**: Shared infrastructure (ingress, monitoring, security)

**GitOps RBAC:** 
- Контроль через Git permissions + ArgoCD Projects
- Каждая команда видит только свои ресурсы
- Централизованное управление через `_main_apps`

Это масштабируемая архитектура для крупных компаний с множественными командами! 🚀