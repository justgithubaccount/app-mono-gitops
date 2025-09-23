### Что заложено в репозиторий `devOwlish/argocd-demo`

| Зона ответственности                    | Что описано                                                                                                                                                    | Где хранится         |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| **Infrastructure-as-Code (IaC)**        | 3 кластера AKS («demo-argocd», «demo-worker1», «demo-worker2»), публичный IP под Ingress, DNS-A-запись в Cloudflare, RBAC delegation                           | `_terraform/…`       |
| **Bootstrap/operational tooling**       | Получение kube-config’ов, Helm-установка Argo CD, запуск GitOps-паттернов                                                                                      | `Taskfile.yml`       |
| **GitOps контроль кластера-управления** | Helm-values для Argo CD (+ self-managed App), регистрация «worker»-кластеров с метками/аннотациями                                                             | `argocd/values.yaml` |
| **Add-on’ы и сервисы**                  | *App-of-Apps* (по одному `Application` на кластер) и **ApplicationSet**-ы (динамическая генерация `Application`-ов для cert-manager, ingress-nginx, reflector) | `patterns/…`         |
| **Cluster state**                       | Все манифесты, values, Terraform коды – в Git → одна точка правды                                                                                              | весь репозиторий     |

---

### Ключевые идеи и как они соотносятся с best practices

1. **Разделение зон**

   * Terraform → отвечает только за облачные ресурсы
   * Argo CD/Kustomize/Helm → отвечает за всё, что «живёт» в Kubernetes API-server.
     Таким образом, инфраструктурная и платформенная команды могут работать независимо, каждую часть откатываем через Git.
     ([kubernetes.io][1], [kubernetes.io][2])

2. **App-of-Apps vs ApplicationSet**

   * *App-of-Apps* удобен как «root» для стартовой иерархии.
   * ApplicationSet (встроен в Argo CD ≥ v2.3) хорош, когда нужно **массово** выпускать одинаковые аддоны на N кластеров или окружений по шаблону.
   * Cluster Generator + метки/аннотации в `argocd/values.yaml` → декларативное включение/выключение аддона на конкретном кластере.
     ([argo-cd.readthedocs.io][3], [argo-cd.readthedocs.io][4], [argo-cd.readthedocs.io][5])

3. **Production-штрихи, которые стоит добавить**

   | Тема                           | Почему важно                                             | Возможный шаг                                                                                              |
   | ------------------------------ | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
   | **Secrets**                    | В репо есть admin-пароль и Azure Client ID → риск утечки | Sealed Secrets / SOPS + Azure Key Vault                                                                    |
   | **Multi-tenancy**              | Сейчас 1 AppProject `default`                            | Разделить Projects по зонам (platform / team-A / team-B) и ограничить destinations & repos                 |
   | **Права к In-cluster Argo CD** | Установлен `server.insecure=true`                        | Включить TLS-терминацию на Ingress и OIDC-RBAC                                                             |
   | **Progressive delivery**       | Сейчас `syncPolicy.automated.prune=true` сразу на всех   | Рассмотреть RollingSync или Git-ops-based canary (Argo Rollouts) для аддонов ([argo-cd.readthedocs.io][6]) |
   | **Image / chart provenance**   | Helm chart версии жёстко зафиксированы                   | Автоматизировать CVE-сканы (Trivy, Azure Defender) и отключить auto-upgrade без валидации                  |
   | **DR & HA**                    | AKS control plane SLA 99.95 %, но Argo CD — stateful     | Репликация `argocd-repo-server` & `redis` через HA-chart или managed Redis                                 |

4. **Обращение к API Kubernetes**

   * Как Terraform, так и Argo CD, Helm, Kustomize в итоге формируют объекты (`Application`, `Deployment`, `Issuer` …) и передают их **API-серверу**, который пишет их в etcd и триггерит контроллеры.
   * Вся автоматизация строится вокруг *declarative desired state* → «состояние кластера = то, что лежит в Git».

---

Отлично, ты как раз работаешь с репой [`devOwlish/argocd-demo`](https://github.com/devOwlish/argocd-demo), и в ней уже заложена **гибридная модель GitOps** с обоими подходами Argo CD:

---

## ✅ Встроено в `argocd-demo`

### 🔁 1. App-of-Apps (начальная иерархия)

> Используется для **bootstrap'а кластеров** и начальной инициализации через `patterns/app-of-apps/_main_apps`.

📄 Пример: [`patterns/app-of-apps/_main_apps`](https://github.com/devOwlish/argocd-demo/blob/main/patterns/app-of-apps/_main_apps)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-argocd
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/devOwlish/argocd-demo
    path: patterns/application-sets
    targetRevision: HEAD
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated: {}
```

🧠 Это корневая точка входа (`root`) — она **разворачивает дочерние ApplicationSet'ы**.

---

### 🔁 2. ApplicationSet (массовые аддоны по кластерам)

> Используется для **массового шаблонного развёртывания** сервисов в разные кластеры (ingress, cert-manager, reflector и т.д.)

📄 Пример: [`patterns/application-sets/ingress-nginx.yaml`](https://github.com/devOwlish/argocd-demo/blob/main/patterns/application-sets/ingress-nginx.yaml)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: ingress-nginx
spec:
  generators:
    - clusters:
        selector:
          matchLabels:
            install-ingress-nginx: "true"
  template:
    metadata:
      name: ingress-nginx-{{name}}
    spec:
      source:
        chart: ingress-nginx
        repoURL: https://kubernetes.github.io/ingress-nginx
        targetRevision: 4.12.3
        helm:
          releaseName: ingress-nginx
      destination:
        name: '{{name}}'
        namespace: ingress-nginx
```

🧠 Все кластеры с лейблом `install-ingress-nginx: "true"` автоматически получают ingress-nginx через этот шаблон.

---

## 💡 Почему это круто и production-ready:

| Компонент                | Используется в `argocd-demo`             | Что даёт                                                                  |
| ------------------------ | ---------------------------------------- | ------------------------------------------------------------------------- |
| **App-of-Apps**          | `patterns/app-of-apps/_main_apps`        | Bootstrap кластера и централизованный entrypoint                          |
| **ApplicationSet**       | `patterns/application-sets/*`            | Масштабируемое развертывание аддонов и сервисов по шаблону                |
| **Labels в кластерах**   | `argocd/values.yaml` (ArgoCD Helm chart) | Автоматическое определение ролей и конфигураций кластеров через селекторы |
| **Taskfile**             | `Taskfile.yml`                           | Скрипты для управления кластером, Argo CD, App-of-Apps                    |
| **Argo CD self-managed** | `argocd/values.yaml`                     | Argo CD управляет сам собой (и всеми остальными) через Git                |

---

## 📦 Что стоит добавить для full-prod:

* 🔐 Перейти на **Sealed Secrets или SOPS + Vault**
* 🔐 Разделить AppProject’ы (по командам или зонам)
* 🌀 Настроить Progressive Delivery (Argo Rollouts)
* 🔭 Добавить Policy-as-Code (Kyverno/OPA)
* 📊 Подключить Grafana + Alerts на ArgoCD app health

---

## 🧠 Вывод

Репозиторий `argocd-demo` — эталонный пример сочетания **App-of-Apps (для инициализации)** и **ApplicationSet (для масштабируемых шаблонов)**. Он:

* Строго GitOps-ориентирован (всё описано в Git → API Kubernetes)
* Делит зону ответственности между Terraform и Argo
* Умеет масштабироваться на десятки кластеров

---

## Хочешь?

Могу:

* Добавить новый ApplicationSet под твои сервисы
* Помочь вынести workloads в отдельный репозиторий (PR-based promotion)
* Настроить Argo Rollouts / auto-updater / Argo CD Notifications

🛠 Сводка на уровне системы:

*Argo CD в этой архитектуре — центральная точка декларативного управления Kubernetes-кластерами через Git, где `App-of-Apps` отвечает за bootstrap и иерархию, а `ApplicationSet` — за масштабируемость и DRY-шаблоны.*
