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
**file:** ./manifests/loki-pvc.yaml
**chunk:** 1/1

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: storage
  namespace: observability
spec:
  volumeName: loki-pv
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/longhorn-system-namespace.yaml
**chunk:** 1/1

```
apiVersion: v1
kind: Namespace
metadata:
  name: longhorn-system
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/chat-api-deployment.yaml
**chunk:** 1/1

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chat-api
  namespace: chat-api
  labels:
    app: chat-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: chat-api
  template:
    metadata:
      labels:
        app: chat-api
    spec:
      volumes:
        - name: logs
          emptyDir: {}
        - name: vector-config
          configMap:
            name: chat-api-vector-config
      containers:
        - name: chat-api
          image: ghcr.io/justgithubaccount/chat-api:latest
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: chat-api-secrets
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 2
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 2
            periodSeconds: 10
          volumeMounts:
            - name: logs
              mountPath: /var/log/chat
          command: ["/bin/sh", "-c"]
          args:
            - |
              uvicorn app.main:app --host 0.0.0.0 --port 8000 \
              | tee /var/log/chat/app.log

          # resources:
          #   requests:
          #     cpu: 512m
          #     memory: 512Mi
          #   limits:
          #     cpu: 1024m
          #     memory: 1024Mi

        - name: vector
          image: timberio/vector:0.47.X-debian
          command: ["/usr/bin/vector"]
          args: ["--config", "/etc/vector/vector.toml"]
          volumeMounts:
            - name: logs
              mountPath: /var/log/chat
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

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/grafana-application.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: grafana
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://grafana.github.io/helm-charts
    chart: grafana
    targetRevision: 9.2.1
    helm:
      values: |
        adminPassword: admin
        service:
          type: ClusterIP
        datasources:
          datasources.yaml:
            apiVersion: 1
            datasources:
              - name: Loki
                type: loki
                access: proxy
                url: http://loki.observability.svc.cluster.local:3100
  destination:
    namespace: observability
    server: https://kubernetes.default.svc
  syncPolicy:
    automated:
      selfHeal: true
      prune: true
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/chat-api-namespace.yaml
**chunk:** 1/1

```
apiVersion: v1
kind: Namespace
metadata:
  name: chat-api
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/chat-api-application.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: chat-api
  namespace: argocd
  labels:
    app.kubernetes.io/name: chat-api
    app.kubernetes.io/part-of: chat-platform  
    app.kubernetes.io/component: backend
    app.kubernetes.io/instance: chat-api
    app.kubernetes.io/managed-by: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/justgithubaccount/app-release.git'
    targetRevision: main
    path: manifests
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: chat-api
  syncPolicy:
    automated:
      selfHeal: true
      prune: true
    syncOptions:
      - CreateNamespace=true
  ignoreDifferences:           # (Best practice для секретов и автогенерируемых полей)
    - group: "apps"
      kind: "Deployment"
      jsonPointers:
        - /spec/template/spec/containers/0/image
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/chat-api-service.yaml
**chunk:** 1/1

```
apiVersion: v1
kind: Service
metadata:
  name: chat-api
  labels:
    app: chat-api
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8000
  selector:
    app: chat-api
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/loki-pv.yaml
**chunk:** 1/1

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: loki-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:  # только для single-node (например, dev-кластеры или minikube)
    path: /mnt/loki-data
  persistentVolumeReclaimPolicy: Retain
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/chat-api-secrets-sealed.yaml
**chunk:** 1/1

```
---
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  creationTimestamp: null
  name: chat-api-secrets
  namespace: chat-api
spec:
  encryptedData:
    CHAT_MODEL: AgA5q2oLd0TI91laazkXZdxKg++MciR0Wss6ftqVdIsMqA33eYfHjwjd1oHtfBvejv37DzyCCVqU6WA/6qh7krac0YOGKcKmnKT3NpvefGvlgP6LQikFUZ5YIQHiEbQXMzZgsWvHfBl7EzDcyDmvHu7AOYfvyKJJiHZSacGSWYsU8mor3AW2DkKqrhiqQBNd9CM5Pv3MHTHf8h8GUuXZU0w0lKCWUznayc5zcz3vpBG9ZHhBYK5H4ErOdIrM+Wsj2ECEW0Urp/do3VKl2sFHvS6ieumdMYyuQMCjJKtG+H3ddNoSABD8ZJcFZE1g2R6tU2xr3GcUrivo6CsQ7oJCWB9lHp7myXY76OwZ5rzTwO1Fh1tl3QhLvlHX4C6lyjZQVMzjS9RkW7G+2I73wf1i1GLB8QYzyThTqLnx4to32Ge7wBAqEIG6rWxwnFguFLceiYB2IQfLmIMHfQBikxlbteLAD2R3odVR+rK+djXLLzR8xyAMd3DZa8lLZXOlhLV7z6gGNO5PMme164wSZnfGxB+h5LsgbcMMIAPR28K16hMG+vYCJOek0bC/J1ML2JcjxaKRbRP43p/aOBo9BeC7hsLLGvXpXsB/Q87+FAZsFyNvE0Q8fCEQH2ToJIIGrQx+A3VqVrz40l3Mz4HOTnHhc0xjeTDzvJzrBwYY1A9A7OmloGbbjhrH0zws3FrfuF+0lYDyUZPS3C8IJ6Z/vn6jAA==
    LLM_API_URL: AgAj/DITXvFik5WFbzgq/SKahwiuPF0EVtrthiXl6jduXuNP7KP3HYZ3Z9qeTMS5t4XEzxXHSsHJhcvQ4qhFWAkT2uSIiT4Zskgn6b6D9I2Izusv4q++ctZqgymLYu/+V5UG18sx5hb/vxUn1b0xmmo6knqXNceX/3jBM469gDt0NUCaOUZsKB4JEL9Psci7bblH4Nup17cp2VE8Ffe7CK9yL/IXDaNJQTTVZ4qWU7egqSxnSqzA7joHFAbCePq9YWDuE3CyxkwNY+df8Hn9uoZRpgM36X9cRSgQese0jlrCL/ykqVBIgwXQ9SDA26+XhlUGlab4pf6zdfp1tPwlPlTBVxOhFtHm5NK7VxUPk9UnNx+wlLQWvx1eymhfpFsaMQpn99ccbZgZ6hZVELrDHJxrOj++itOWs8spu7FyS4spA/CM6IKbEU3oKu5i2EX7U7dVZ3ZmPCJ53hcFc8P92ZT9Wukx55tt6ZklVtQI/hR0wBhfEmgOgMdyQHC7Ejpi3V9dLUfKEHaPgPWrMrPREt5HGg87Jmy2oIjH4W0/yObKyIXsW58HVnbAG/8Yzxd2aSfpKxma0sUAHLfNh1tYgVFFyrK99/LPU2hQ6NXT6nS5aB2xtyPtRXFkgy+aT1zq46uIBp+zqBJQoQD2dVowORXl875KquLhq4XVP/F3Nw2avlt+qWL8IOQmKY+Mg3MaywB/Y4le2qkNHeoClgEbU2rSRFxf
    OPENAI_API_KEY: AgBSoj+r1/38ZgRPXeH6oEhGSH3zeLARgyTA1agGW0E+xNdCIhfZJS+wZVvCLsYwhOyzrbkNIoKV+uEWbskj4iuNghI/sNaKxign0k6IEOpPbECTydBBBZK/uveGiuRcQBZpPnT5zYosh2jW9fHmutgWg1eu48VDBzJO4gbTENXEa3G6fCdFyLDsBRbMQzErbrwMxhQbwl0mUqOyflCArVhuKDEDM8FU30SD71iYQLjoakR8jdULSV935yHi/a7HJ78wzd2E8xHCYTCfeTsgfbpxMFUVWU+uCLGp/7zK4+eSEfmdw0JqmCleKIU1JtASvLgPxQpY4PGEUBov05eVUbq8jy3GY/8VUOKhsdIRIuLVI9u/GIVCABxTs7LOXHpAleyp5cnI7CZ2gebdGMJoha6ROd16kbO/GqJKfaEbIjalsOf8lCvfZO+4zLrIsGu0aC7vhcqMfBZP7qm5g9W7vY20BTTDKU8uq09BPz19CbEuIyYnEqAPuK4kz3C4N4sV97DHVIadGQxrcmaviP7evvdlVpg5+GWQPGtRJJ4nQz53sEftzNdvxCYOnSarFhYannHfsVYC5EjEYb4RG8OLHV95xexKleL1RY7mfkQg/D+Edd+DiiPoYl2mr9WHM0XAj8PG4fwd38nLcsBvVPlprHKzfc7acnG2ovaOGcmH0ECQ9xxNzjqzAHg03qokU02Br3OIloSManal6zBKTetIHkWO77tB4meKPAbq2yaKrnZZhL/LheLTfLd7xjd0+QrvS7QU02VkDuBNLTXnMmoUNuVYlCtM9NYaBBzo
    PROJECT_NAME: AgA/GFFaBselJr5OpPYrB7iUXzxod5vPCh4c4zegr4LD8DefVPLz1Pz5EDYMp/JI2EeqnhzuLnBrkmW6TMyCLo8yTKf5117Ho+zF1J1cZtvYWfACM7SLO5ZnKOBzezx2gBaTv+/u+J/TkaF1J9L3UdR3dTkCNfs8Krh/mafKf0hPQz7ndlx6qfVvsgkP/tg5u9rrKemvqpJXUNHZaclbhKqhXxOAQ4QsXwJlSTirz0Rtutoh3U8zTJ7x/M6Jo4+S2xSV+zQPssxaMNa2M8NBnFMGsTVb7Gri5vrWVWgkAFmmTe1ZuVYHaSGW9rcSn7Wfgze6hS/mgfsDyNHE73utWPGj0MiyHgy+KVvBXmOdJ+h65+hq6KdLFzkH8D3R9ZVgnx4jVuop26SauDisGEg5tYvbpHdZV4mOMXQ2UFJcRaHO2P1T7cqxtINN34PQPWQM5UxDvOHSbas9XwwH3i6jmxjwe0Fo7otkHnTznUaZtIFR+6vlXAYjBUW76M2nrjKLCnSp5G4/uEQhfH47A5s24i7oZNKbG70YLwCOOlUR6sf33yJuTRVJHTOxrJ36GAHTwPIqkik7+jZByXkaE0G6OJO7uDq2m6PdK1YqSfSxP2ea0rQI3DBE/Ho7ujb45ThqNeQ5iAbUUHaCnq/ksr6zWC2A6bgfUqK4G9+BAltxkVaVkZfdeg5C0rU5OzCWHd5CSnLRlNz5GBjeTfrPh7GeZ/Ry
  template:
    metadata:
      creationTimestamp: null
      name: chat-api-secrets
      namespace: chat-api
    type: Opaque
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/loki-secrets.yaml
**chunk:** 1/1

```
apiVersion: v1
kind: Secret
metadata:
  name: loki-s3-secret
  namespace: observability
type: Opaque
stringData:
  access_key: "LT98WU4OFJ3TL306KONR"
  secret_key: "3RlOKpwnCx2MktBqiui2XS4OxBeI3P0f9QM1NzTG"
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/litellm-secrets.yaml
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
**file:** ./manifests/litellm-vector-configmap.yaml
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
**file:** ./manifests/litellm-secrets-sealed.yaml
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
    OPENROUTER_API_KEY: AgA+ACa5Lc/PPwGr3RiFmArBr8q7p0R+9w0KdVzgsyhOp6LoNuIYYQDpTwSEz0TZgXpAeunajIBTVmIPHJmfkbSKkv1JYzrUk01N4b5iQrxzp+hKtFa7TonqC70YlNeIVMPWRNrkU6NALQd5gCC64JQ1nlW5/cZzV56qc8irALbYAAZYcdikp6mLSA0ZDNbIveIPXcYJrJuGjO+9oKF09ICui1xTUjDiDxSxiq5k1GRQTAesRIWt2PGONSqXJFEVAbcV6FdTunYGJjdEyzEjzvPS9GDdvLGdjxeg1hNvKzWLVrQaUDJ6Ms9PoCcme09nEXTDtCHQcipULQ00IQIZ2tt5dkU1ELxJlkg7HS5+a+s0FU3XT5RSEinPQtYTrT7rn0ZGJt8QCr8iaiBiBcicvw020SgyP9K8D1vklkUMFw03ZHlY8oQ38QF3Q7eAqIvdX22Tjj0iuT/7NGj4dTJrlkZZWAWt1ZW+pe14H/LT8dfb/+VT1Kexv0Ln/gA8ozKqDt9UBasl6ZulB5BBgcf9Q2PUB3C6dcSlOjoXRCS1KuKbMQ1DTVNIQnsxUYGr0iAG1gI3YFmUWkzHpqmOBhlzxNRkF5h9IXPlXaiEMpdIyMDvWyIU9TeFOXwSLm6Tk5Kigq36qKmU9jGHHAS8O2HWZwbp1ZlfTXNnzEMuAAPtwifsayPoimbGy6Cz00Szm827WkOvFJx8E6/4XoZVeVGx+w/6hbh90Nd2VGeQmNRKcJd9SGZ2LMcf3RHL5/UOtX2DvSWgkYLQVMvy3z3Ox5Dk7yEopn6IVBgV0WKH
  template:
    metadata:
      creationTimestamp: null
      name: litellm-secrets
      namespace: chat-api
    type: Opaque
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/grafana-ingress.yaml
**chunk:** 1/1

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: grafana
  namespace: observability
spec:
  ingressClassName: nginx
  rules:
    - host: grafana.syncjob.ru
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: grafana
                port:
                  number: 80
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/chat-api-ingress.yaml
**chunk:** 1/1

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: chat-api
  # annotations:
  #   nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: chat.syncjob.ru
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: chat-api
                port:
                  number: 80
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/litellm-service.yaml
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
**file:** ./manifests/litellm-configmap.yaml
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
**file:** ./manifests/chat-api-vector-configmap.yaml
**chunk:** 1/1

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: chat-api-vector-config
  namespace: chat-api
data:
  vector.toml: |
    [sources.file_logs]
    type = "file"
    include = ["/var/log/chat/*.log"]

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
    labels.app = "chat-api"
    labels.env = "public"
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/chat-api-secrets.yaml
**chunk:** 1/1

```
apiVersion: v1
kind: Secret
metadata:
  name: chat-api-secrets
  namespace: chat-api
type: Opaque
stringData:
  OPENAI_API_KEY: "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"
  LLM_API_URL: "http://litellm:4000"
  CHAT_MODEL: "openai/gpt-4.1"
  PROJECT_NAME: "ChatMicroservice"
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/loki-application.yml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: loki
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://grafana.github.io/helm-charts
    chart: loki
    targetRevision: 6.30.1
    helm:
      values: |
        deploymentMode: SingleBinary

        singleBinary:
          replicas: 1
          persistence:
            enabled: true
            storageClass: longhorn
            size: 10Gi

        backend: { replicas: 0 }
        read: { replicas: 0 }
        write: { replicas: 0 }
        ingester: { replicas: 0 }
        querier: { replicas: 0 }
        queryFrontend: { replicas: 0 }
        queryScheduler: { replicas: 0 }
        distributor: { replicas: 0 }
        compactor: { replicas: 0 }
        indexGateway: { replicas: 0 }
        bloomCompactor: { replicas: 0 }
        bloomGateway: { replicas: 0 }

        gateway:
          enabled: false
        lokiCanary:
          enabled: true
        test:
          enabled: true
        grafana-agent-operator:
          enabled: false
        resultsCache:
          enabled: false
        chunksCache:
          enabled: false

        loki:
          auth_enabled: false
          commonConfig:
            replication_factor: 1
          pattern_ingester:
            enabled: true
          limits_config:
            allow_structured_metadata: true
            volume_enabled: true
          ruler:
            enable_api: true
          storage:
            type: s3
            bucketNames:
              chunks: ceae9495-3a627f83-8eba-441e-b648-37d41cded627
              ruler: ceae9495-3a627f83-8eba-441e-b648-37d41cded627
              admin: ceae9495-3a627f83-8eba-441e-b648-37d41cded627
            s3:
              endpoint: s3.twcstorage.ru
              access_key_id: ${S3_ACCESS_KEY}
              secret_access_key: ${S3_SECRET_KEY}
              region: ru-1
              insecure: true
          schemaConfig:
            configs:
              - from: "2024-04-01"
                store: tsdb
                object_store: s3
                schema: v13
                index:
                  prefix: loki_index_
                  period: 24h

        extraEnv:
          - name: S3_ACCESS_KEY
            valueFrom:
              secretKeyRef:
                name: loki-s3-secret
                key: access_key
          - name: S3_SECRET_KEY
            valueFrom:
              secretKeyRef:
                name: loki-s3-secret
                key: secret_key

  destination:
    namespace: observability
    server: https://kubernetes.default.svc

  syncPolicy:
    automated:
      selfHeal: true
      prune: true
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/loki-secrets-sealed.yaml
**chunk:** 1/1

```
---
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  creationTimestamp: null
  name: loki-s3-secret
  namespace: observability
spec:
  encryptedData:
    access_key: AgCSUHVpJj6uUVIn4W68tFvlnEBjF91ZwQYHNnd3m5Vo/bFvpBVOmmv7Ix+t83ZCWWqQIV40FwJAKXJpMTymFR9JcgM54Ah+1aR2ueSs0uWERMeHsTnZwJNym0Wgu6Am/TcbPxiq1HCoxPVem+Ifs4hzzui3rmUIvF945C91Nllw20K/ZQ5lbR6sK55rntCX5Jb1FESnYa8O+RSbcUH8t/omWyzvQTirty+8yUCDl3OOQXPKy/8P3qoIibaQypX3zx4vD+S0X6cTk7+E72jWDKyWDMWgyMstQCzbjqIOQ4q4P4zOgr3jMRPr895lx4bTqcXh0l7Mw14HdVgVM9L4t+nhR9bqbvzLGhRrK1hNhZBKf4HIiGKPqQSXOv+GDkpGwT87qI7lJ8JRQZVRc0Ih3UE1fhddX8mzMOChPcB5GQCvSA1EwyQRydch8HqEVmRq0VfTjsfzNjAkrPf+oi+pEfkRzxgc4DoTyPIYz6+xi/5jHBP43evM0ipTllq0VMd0yx9iOmZg6u0GpA6toI04c50CIMu93WvmpVQbiwNepG/EwB0+357gRwQ00LpENhidygr3E24xbBAXC8Nae7f6RUwZOglkvwb38S2lyGXCCMNlRNKpzuHFAxyvlMZ/NlaUE+UNajN/6vW5dlXAXxWAsfoXmyv0nb4lCxYarZYyUoIkNNA6FTVsqMcxXjnYEc8iWGuU77IzE1q+V0waNxkRKEmKT2bdNA==
    secret_key: AgCokcdzMap0skKeQ4yboL+hO0aIBQExe27pnOmf9kFwKTFVNOCdVLQPdDBtw4qvoHfjyBPkEZKTcWU0FmOCfeRfIvA4KiW9hwa/WaezAE1nnduEiQyLBB8XtCmFCUlD8pFK2KUD1hpLMnqrpKLQQGA103OrKdrTU3bofdKNHPHrjoS4pwTgAvzK3fnRHbvISUixi5quTWaNrwm57RgauisR/8eMvTyUo33TuNmCcj+/4KrCMZ9TTv0JwT4aY51rb0z3VrwKoPzcG+6GeyOzhktov9xID1JfjBDsHwu6wTqOgi4g7/00p7FniNDVDMhO2DmzdkaAOlmNEh7vY5vMN/mw+f0AlsjEUJ9uYwstWQ6Eu69pAJzhRA9ORIw0HXKgwO/ZBkHR1r3rF9uysraUvKRUEF4s6+zH9lC8iLgB7dgesFZI4TZpXJ8Gl+EUIqsG/fJyuQleFZhY/d45yok1SRbhEPvofPnt5j3/K2R8o+VJ/f1t9P/zF6jTvGLcFWmWSIqBASW0zHLxLt1jwy8YkizaoNvdeic933ofccjRciMiLEpjrIyeFFdd3y4Jf5SrAbSXHGszme+O/hGoM4DixQyqOHhNcAhdGw5zgJmOnhJea70sXq4O2j/pX9TtkrDhc7B6LmzkOX/b1iVRd35yuqnEgVpJYI63XxZe2OnOeRBTvR36HmYpaq4Dem8R+PxI4hkbL5BCG1ArBrhdR5nygblzncNTJ+sAqKdwlsfRs/Ow5g/ODwR3r7ai
  template:
    metadata:
      creationTimestamp: null
      name: loki-s3-secret
      namespace: observability
    type: Opaque
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/longhorn-application.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: longhorn
  namespace: argocd
spec:
  destination:
    namespace: longhorn-system
    server: https://kubernetes.default.svc
  project: default
  source:
    chart: longhorn
    repoURL: https://charts.longhorn.io
    targetRevision: 1.9.0
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/observability-namespace.yaml
**chunk:** 1/1

```
apiVersion: v1
kind: Namespace
metadata:
  name: observability
```

-------------------------------------------
**role:** config-yaml
**file:** ./manifests/litellm-deployment.yaml
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

