# 📦 CREWAI/AI-КОНТЕКСТ: ПРОЕКТНЫЕ ФАЙЛЫ

Это экспорт файлов из проекта для передачи искусственному интеллекту или агенту (например, LLM или crewAI).  
Здесь каждый файл разбит на **чанки** — отдельные куски данных, чтобы AI мог эффективно читать, анализировать и строить ответы на их основе.

---

### 🤖 Зачем это нужно?

- Большой проект невозможно отправить AI-агенту целиком — его "контекстное окно" ограничено.
- Файлы делятся на логические части ("чанки").
- У каждого чанка есть метаданные: роль, путь, тип, номер чанка.
- В таком виде проект можно анализировать, рефакторить, строить документацию или делать автотесты силами ИИ.

---

### 🧩 Что такое "чанк"?

**Чанк** — это кусок файла ограниченного размера.  
Так проще пересылать и обрабатывать большие данные.

---

### ⚙️ Как устроен этот экспорт?

- Пробегаемся по проекту, исключая техпапки (.git, node_modules, ...).
- Для каждого файла определяем его роль по расширению.
- Если файл большой — делим на чанки.
- Каждый чанк оформлен в markdown с подписями.

---

-------------------------------------------
**role:** config-yaml
**file:** infra/base/services/llm/gateway/kustomization.yaml
**chunk:** 1/1

```
resources:
# - application.yaml
- litellm-configmap.yaml
- litellm-secrets-sealed.yaml
- litellm-vector-configmap.yaml
- litellm-deployment.yaml
- litellm-service.yaml
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/services/llm/gateway/litellm-secrets.yaml
**chunk:** 1/1

```
apiVersion: v1
kind: Secret
metadata:
  name: litellm-secrets
  namespace: chat-api
type: Opaque
stringData:
  OPENROUTER_API_KEY: "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"
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/services/llm/gateway/litellm-vector-configmap.yaml
**chunk:** 1/1

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: litellm-vector-config
  namespace: chat-api
data:
  vector.toml: |
    [sources.file_logs]
    type = "file"
    include = ["/var/log/litellm/*.log"]

    [transforms.parse]
    type = "remap"
    inputs = ["file_logs"]
    source = '''
    . = parse_json!(.message)
    '''

    [sinks.loki]
    type = "loki"
    inputs = ["parse"]
    endpoint = "http://loki.observability.svc.cluster.local:3100"
    encoding.codec = "json"
    labels.app = "litellm"
    labels.env = "public"
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/services/llm/gateway/litellm-secrets-sealed.yaml
**chunk:** 1/1

```
---
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  creationTimestamp: null
  name: litellm-secrets
  namespace: chat-api
spec:
  encryptedData:
    api-token: AgCdEKe0ivGzhK4badmV+dWYq8bCdWK3zkzcaf0N6L0L2Na6GJRA37ofmakSn81HE0fi72WmmcEpcLGMYHZxk6UceO9qvPPIm7i5fk5qdJ9zLgLp2RiqdgiypJuuRCSq3ikpReabVg9K6AbYoGIUJdv7not+k+g6CqNKOl6jMr3DDJ2Y5k4PnoaEuVruxoYCOlq0mIqszZjS++kPTuCcK1XV3DjmU2SUemITaYfiu1VhewlS2sWcU3QB7FB67JbOpXLFAihmeA0+zY/cwvk41ex9EDNxxnJewMht4KC4/EYpiDlnSSSnOgLJmEDOVbJd7zlPsHX/L0b6S5gYXCosx0kKZn1o1U6VuX6uJpyn2Bn0EYANfvIByhwjhn7pHWxCtxv4mSSRjpsHbNban7oFTcRu4g4WOUcgUYHs5c4ojQNZtVCBHKtvhIUUYp+HWf0td0SZcLevKvKoiAMP3u/ljHWLJXo7UeQIoaVIrHJ1b30vyJn3huQyOCmOkwUj2xg+/XpjVLObDvTuqo51Dr1oUZguZ4yGb7Gw195jB+90FqYrP3gi1up2CzlRC2KgfKJ8E4EhalC049IbKtPhvyMCWjTx5aennYKfn68ZkCVUqQ7V8CiStFm/eoK2ORhZydczRpq10504bKX/qaUqlS5ef+qNn0MQCbWrp3eocbQ0re5BOMf5bRcTibk/OPTo7Ok4ZFiNcBVWZm9igekdT9v3dQi1Nf6T04ndOhbF2javb7ry3EOwWkfM33/c+mGWmkeVgXI7Uemmi7NQFhd78AhW5GKmZvZO71f0JXht
  template:
    metadata:
      creationTimestamp: null
      name: litellm-secrets
      namespace: chat-api
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/services/llm/gateway/litellm-service.yaml
**chunk:** 1/1

```
apiVersion: v1
kind: Service
metadata:
  name: litellm
  namespace: chat-api
spec:
  selector:
    app: litellm
  ports:
  - protocol: TCP
    port: 4000
    targetPort: 4000
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/services/llm/gateway/litellm-configmap.yaml
**chunk:** 1/1

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: litellm-config
  namespace: chat-api
data:
  config.yaml: |
    model_list:
      - model_name: gpt-4.1
        litellm_params:
          model: openai/gpt-4.1
          api_base: https://openrouter.ai/api/v1
          api_key: os.environ/OPENROUTER_API_KEY
          api_key_header_name: Authorization
          api_key_prefix: "Bearer"
    litellm_settings:
      set_verbose: true
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/services/llm/gateway/application.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: llm-gateway
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/justgithubaccount/app-release
    targetRevision: HEAD
    path: infra/base/services/llm/gateway
  destination:
    name: CLUSTER
    # server: https://kubernetes.default.svc
    namespace: chat-api
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/services/llm/gateway/litellm-deployment.yaml
**chunk:** 1/1

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: litellm
  namespace: chat-api
  labels:
    app: litellm
spec:
  replicas: 1
  selector:
    matchLabels:
      app: litellm
  template:
    metadata:
      labels:
        app: litellm
    spec:
      volumes:
        - name: config
          configMap:
            name: litellm-config
        - name: logs
          emptyDir: {}
        - name: vector-config
          configMap:
            name: litellm-vector-config
      containers:
        - name: litellm
          image: ghcr.io/berriai/litellm:main-latest
          ports:
            - containerPort: 4000
          envFrom:
            - secretRef:
                name: litellm-secrets
          volumeMounts:
            - name: config
              mountPath: /app/config.yaml
              subPath: config.yaml
            - name: logs
              mountPath: /var/log/litellm
          command: ["/bin/sh", "-c"]
          args:
            - "litellm --config /app/config.yaml > /var/log/litellm/app.log 2>&1"
          # resources:
          #   requests:
          #     cpu: 100m
          #     memory: 128Mi
          #   limits:
          #     cpu: 300m
          #     memory: 256Mi

        - name: vector
          image: timberio/vector:0.47.X-debian
          command: ["/usr/bin/vector"]
          args: ["--config", "/etc/vector/vector.toml"]
          ports:
            - containerPort: 4317
              name: otlp-grpc
          volumeMounts:
            - name: logs
              mountPath: /var/log/litellm
            - name: vector-config
              mountPath: /etc/vector
          # resources:
          #   requests:
          #     cpu: 50m
          #     memory: 64Mi
          #   limits:
          #     cpu: 150m
          #     memory: 128Mi
```

