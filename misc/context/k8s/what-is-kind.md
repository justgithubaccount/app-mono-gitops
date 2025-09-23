🔍 Отлично, давай разберём:

> **"Сколько стандартных объектов (kind) есть в Kubernetes?"**  
> И **да**, каждый `kind` — это отдельная **ручка (endpoint)** в REST API Kubernetes.  

---

## ✅ Что такое `kind`?

* Это тип объекта в Kubernetes API, например:

  * `Pod`
  * `Deployment`
  * `Service`
  * `Node`
  * `Namespace`
  * `ConfigMap`
  * `Secret`

> Всё, что ты создаёшь в YAML — это объекты с полем `kind`, которые имеют свой endpoint в API-сервере.

---

## 📎 Пример одного объекта:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
```

💡 В kube-apiserver это → ручка:

```http
POST /apis/apps/v1/namespaces/default/deployments
```

---

## 📚 Сколько `kind` по умолчанию в Kubernetes?

Зависит от версии, но:

### На сегодня (пример: Kubernetes v1.29):

* Примерно **60–100+ стандартных `kind`**
* Они разбиты по **API-группам**:

| API Group                   | Примеры Kind                                       |
| --------------------------- | -------------------------------------------------- |
| `core` (aka "" group)       | `Pod`, `Service`, `ConfigMap`, `Node`, `Namespace` |
| `apps`                      | `Deployment`, `StatefulSet`, `ReplicaSet`          |
| `batch`                     | `Job`, `CronJob`                                   |
| `networking.k8s.io`         | `Ingress`, `NetworkPolicy`                         |
| `rbac.authorization.k8s.io` | `Role`, `ClusterRole`, `RoleBinding`               |
| `policy`                    | `PodDisruptionBudget`, `Eviction`                  |
| `autoscaling`               | `HorizontalPodAutoscaler`                          |
| `storage.k8s.io`            | `StorageClass`, `CSIDriver`                        |
| `apiextensions.k8s.io`      | `CustomResourceDefinition`                         |

И т.д.

---

## 🔧 Как посмотреть все `kind` у себя:

```bash
kubectl api-resources
```

Пример вывода:

```text
NAME                SHORTNAMES   APIVERSION                             KIND
pods                po           v1                                     Pod
services            svc          v1                                     Service
deployments         deploy       apps/v1                                Deployment
configmaps          cm           v1                                     ConfigMap
cronjobs            cj           batch/v1                               CronJob
...
```

---

## 🌐 Альтернатива: REST API напрямую

Можно дернуть ручку:

```bash
kubectl get --raw /openapi/v2 | jq '.definitions | keys[]' | grep -v '\[' | wc -l
```

Или:

```bash
kubectl get --raw /apis
```

Там будут все `groupVersion` → потом `resources`

---

## 💡 Каждому `kind` соответствует ручка:

| Kind       | HTTP endpoint                                  |
| ---------- | ---------------------------------------------- |
| Pod        | `/api/v1/namespaces/default/pods`              |
| Deployment | `/apis/apps/v1/namespaces/default/deployments` |
| Ingress    | `/apis/networking.k8s.io/v1/ingress`           |
| Node       | `/api/v1/nodes`                                |

> Всё чётко укладывается в REST:  
> `apiVersion` → URL  
> `kind` → тип объекта  
> `metadata.name` → ID  

---

## ✅ Сводка:

* Каждый `kind` — это **объект и ручка** в REST API kube-apiserver
* Всего в Kubernetes (v1.29) — около **100+ встроенных kind'ов**
* Можно получить список через `kubectl api-resources`
* Можно обращаться к ним напрямую через HTTP (ArgoCD, SDK, curl)

---

Хочешь — могу показать, как выглядит прямой `curl` к `kube-apiserver` с аутентификацией, или собрать список всех kind с описаниями по группам.
