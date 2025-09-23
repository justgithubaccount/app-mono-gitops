Отлично. Разложим **полный жизненный цикл `Deployment` в Kubernetes**, начиная от `kubectl apply` или ArgoCD push до запуска контейнеров на ноде — с акцентом на **REST API**, **контроллеры** и **etcd**.

---

## 🔄 Жизненный цикл `Deployment` пошагово:

---

### 📥 Шаг 1. Git → ArgoCD → kube-apiserver

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:latest
```

👉 **GitOps:**
ArgoCD делает `kubectl apply` или `PATCH/PUT`:

```http
POST /apis/apps/v1/namespaces/default/deployments
Content-Type: application/json
```

* API-сервер валидирует объект по OpenAPI-схеме
* Сохраняет его в **etcd**

---

### 🔁 Шаг 2. Включается **Deployment Controller**

Контроллер подписан на события по типу `apps/v1/Deployment` через `WATCH`.

Он:

* видит, что `Deployment` `my-nginx` создан
* генерирует и создаёт соответствующий `ReplicaSet`:

```http
POST /apis/apps/v1/namespaces/default/replicasets
```

* ReplicaSet получает имя вроде `my-nginx-5f7dd7b78c`

---

### 🧠 Шаг 3. ReplicaSet Controller запускает `Pod`’ы

Контроллер `ReplicaSet` видит, что у ReplicaSet:

* `spec.replicas = 3`
* и нет подов

Он:

* создает 3 Pod-а на основе `.spec.template` из Deployment:

```http
POST /api/v1/namespaces/default/pods
```

Все 3 Pod-а сохраняются в etcd.

---

### 🧭 Шаг 4. Scheduler выбирает ноды

Контроллер `kube-scheduler`:

* получает список Pending Pod-ов (без `nodeName`)
* выбирает подходящие ноды
* патчит Pod, добавляя поле `spec.nodeName`:

```http
PATCH /api/v1/namespaces/default/pods/nginx-xxxx
{
  "spec": {
    "nodeName": "node-1"
  }
}
```

---

### 🖥️ Шаг 5. kubelet на ноде запускает контейнер

`kubelet` на `node-1`:

* читает список pod-ов из API
* видит, что ему надо запустить pod `nginx-xxxx`
* вызывает `containerd` или `cri-o` для запуска контейнера `nginx:latest`
* монтирует volume, создает sandbox, настраивает сеть и запускает

Когда контейнер готов, kubelet отправляет статус обратно:

```http
PUT /api/v1/namespaces/default/pods/nginx-xxxx/status
```

---

### 🟢 Шаг 6. Всё готово

* Pod работает
* ReplicaSet доволен (у него нужное число ready pod’ов)
* Deployment доволен (у него нужный ReplicaSet)

**Система самобалансирующаяся** — если pod упадёт, всё запустится заново.

---

## 📡 Обновление Deployment

Если ты меняешь `.spec.template.containers.image`:

```yaml
image: nginx:1.25
```

Контроллер `Deployment`:

1. Создаёт **новый ReplicaSet** с хэшем по новому `template`
2. Постепенно уменьшает `replicas` у старого RS
3. Увеличивает у нового (Rolling Update)
4. Управляет стратегией через `progressDeadlineSeconds`, `maxSurge`, `maxUnavailable`

Всё снова через API и etcd.

---

## 📊 Визуально (по шагам):

```text
[Git]
  ↓
[ArgoCD → REST]
  ↓
[kube-apiserver] ←→ [etcd]
  ↓             ↑
[Deployment Controller] — создает ReplicaSet
  ↓
[ReplicaSet Controller] — создает Pods
  ↓
[kube-scheduler] — патчит nodeName
  ↓
[kubelet] — запускает контейнер
  ↓
[status → apiserver → etcd]
```

---

## ✅ Сводка уровня системы:

| Элемент        | Что делает                                      |
| -------------- | ----------------------------------------------- |
| kube-apiserver | REST API, валидация, общение с etcd             |
| etcd           | Хранит всё состояние                            |
| Deployment CR  | Определяет желаемое состояние                   |
| Controllers    | Следят за CR и синхронизируют текущее состояние |
| Scheduler      | Назначает ноды для подов                        |
| kubelet        | Реально запускает контейнеры                    |

---

Хочешь — покажу live пример через `kubectl apply` и `kubectl get events` как эти действия происходят в реальном времени.
