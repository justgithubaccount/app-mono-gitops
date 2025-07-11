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
**file:** infra/infra-root.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: infra-root
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/justgithubaccount/app-release.git
    path: infra/_roles
    directory:
      recurse: true
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/services/postgree/pg-secrets-sealed.yaml
**chunk:** 1/1

```
---
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  creationTimestamp: null
  name: chat-api-db
  namespace: chat-api
spec:
  encryptedData:
    DATABASE_URL: AgA27eUSEHIdkBgWhx0KMCrZnu8aihSG9cfZhcSVdcyV/v+QDpAih8oQqsO/qq6EhBadzMwoxymLN/zdvZIPGc+m+07mACB2hgtxy/1wIB4EkFoT0fY+hnNMvjCG5RW2mVpGTvOf2dLlE/qJBCrtsCotYybancuMrGkft0RbRBahBqQJd6gcWPwNjN2c6euvTNYypGbFSsnQ48ynk6JAcqEbeOKJ01QY5oCOA76knOchzPjya8/wzECWE8tJonzDA0OTjoOnKAOqcOwyrPpzfelRVx8PRaGy3PHTPBD0pbxy0i90OSYt5dCGMqa+6DXHOz4EO+o1dbKmULjVSeUr8H9lzAZRyXpXDpSIvQii91U8hNpIsukMvwHZGq4DYKpbChSpLaVi30Q0kJWx8Ro2bMakcTSGzhHr2a4ldTy0c4yC6a7riYCB4CGyTpqj/W6Q9BG2wOqjZyd7hqiOJKpUARvFosTo1UoxQAqiKLLgpdEnn1txDaeJm51HlMdI2V0g5QCB0uobqDydaVy7XP0NtSYx8xuEX7eRqYyrQOz4NiSNBxAOwvB08urUMQdaZ4ayHgs5cP0o/GDMpUHzkBYldJuvJ+vcLNx+NillmxACj0cQ4b44yQklONRurQy2gTVxkJqWxmhSHN3eS+G1pgEjzTqIusKLizCEzBVW+dRlctgTUm4Ix4vG+WhbfVoqFVsN+NDy17+/X2+HMIzuwfuSsunk0Ubcj9uO9cVIfrdl5bcgUX2IX/gp10c7qIptGEWr20K2lvClnoxGiBVFZ0fgM/c=
  template:
    metadata:
      creationTimestamp: null
      name: chat-api-db
      namespace: chat-api
    type: Opaque
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/services/postgree/pg-secrets.yaml
**chunk:** 1/1

```
apiVersion: v1
kind: Secret
metadata:
  name: chat-api-db
  namespace: chat-api
type: Opaque
stringData:
  DATABASE_URL: "postgresql://gen_user:(=9AW^n*tJ$_X@192.168.0.4:5432/default_db"
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/services/agent/chat/kustomization.yaml
**chunk:** 1/1

```
resources:
  - application.yaml
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/services/agent/chat/application.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: chat-api
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "4"
spec:
  project: default
  source:
    repoURL: https://github.com/justgithubaccount/app-release
    targetRevision: main
    path: charts/chat
    helm:
      values: |
        image:
          tag: latest
  destination:
    # server: CLUSTER
    server: https://kubernetes.default.svc
    namespace: chat-api
  syncPolicy:
    automated:
      selfHeal: true
      prune: true
    syncOptions:
      - CreateNamespace=true
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/services/llm/gateway/kustomization.yaml
**chunk:** 1/1

```
resources:
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
    OPENROUTER_API_KEY: AgCtOOFnF+WQaWT9wp+c6utBGdSgk8IprflgDXcVUZZJ0dXuEyzWVrpLHLqFDaijUNNh4izjezQOSTDbNxLef22sIHiNWVJuGJpZe5zUq48e2ql3+39C7Xf0ELbPgBox/r+lw48EDrVsbxQhCJzhIScX4vvhqs7ZAwhJiw4Y63ECzrEw0VFG4+HIJdtnuJfTU40SVBHOaajWEf4ocWOLL7p/5NQotg7kWG1D+Oo4N0XXiKdmHANRINQvl2FVnG6Vu9OHCr/kql6qCrDEjTOHIGvuC9fy+dnbvILR470v54E2WIwtDnMK4dMaXluYXeftP3jvWABMkkYB/1FqpURnSHigVIwojRAVGmp8K+fTQsW01TUoKkbMxWtaqKpeXJKl6UubvO73+D8B/+d0pY8KtooPXlWB7xbBPC2zPqyZYQSBUWMPT5eZ9bt4xrbSwLo9GAuAyhvI1+rFMkZXCDFw0T6cqM6H1JeHiX9+oSSDkE28lq884Rr3V+IB7VOegSKNm5cf5r+nYtDq8hHiyqNuuXaA+/TNMiTw6roHeTogizy0GprYYYXJLBFEG1KaJyl25h5d1iJZXp7AyomUk4RS21jxU3L+Hm5XcmiOAVu6PZANU1QDzp53CrPugV4JZ5loOBUJ49SOIz0EYF8VyHdOLqBZMABNU+IfeU5XmN9lrxt1idQZcpqSzQAZTOGQWcMXBORpGw78B7/hG5be6aOo4jSwPprkDWVMWfOzYcKxc52XEy2m/xfh0Vl/l/puvr3GgIHeAV58u7KB+KBoe52SZNgLuYDANZaZAwj6
  template:
    metadata:
      creationTimestamp: null
      name: litellm-secrets
      namespace: chat-api
    type: Opaque
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
    repoURL: https://github.com/your-repo/app-release
    targetRevision: HEAD
    path: infra/base/services/llm/gateway
  destination:
    server: https://kubernetes.default.svc
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

-------------------------------------------
**role:** config-yaml
**file:** infra/base/issuer/issuer-cluster.yaml
**chunk:** 1/1

```
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-dns
spec:
  acme:
    email: kulikovyevgeny@outlook.com
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: letsencrypt-dns-key
    solvers:
      - dns01:
          cloudflare:
            apiTokenSecretRef:
              name: cloudflare-api-token
              key: api-token
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/addons/observability/grafana/kustomization.yaml
**chunk:** 1/1

```
resources:
  - application.yaml
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/addons/observability/grafana/application.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: grafana
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "2"
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
**file:** infra/base/addons/observability/loki/loki-pvc.yaml
**chunk:** 1/1

```
# apiVersion: v1
# kind: PersistentVolumeClaim
# metadata:
#   name: storage
#   namespace: observability
# spec:
#   volumeName: loki-pv
#   accessModes:
#     - ReadWriteOnce
#   resources:
#     requests:
#       storage: 10Gi
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/addons/observability/loki/kustomization.yaml
**chunk:** 1/1

```
resources:
  - application.yaml
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/addons/observability/loki/loki-pv.yaml
**chunk:** 1/1

```
# apiVersion: v1
# kind: PersistentVolume
# metadata:
#   name: loki-pv
# spec:
#   capacity:
#     storage: 10Gi
#   accessModes:
#     - ReadWriteOnce
#   hostPath:  # только для single-node (например, dev-кластеры или minikube)
#     path: /mnt/loki-data
#   persistentVolumeReclaimPolicy: Retain
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/addons/observability/loki/application.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: loki
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "2"
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
**file:** infra/base/addons/observability/loki/loki-secrets-sealed.yaml
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
**file:** infra/base/addons/longhorn/app-longhorn.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: longhorn
  namespace: argocd
spec:
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
  project: default
  sources:
    - chart: longhorn
      repoURL: https://charts.longhorn.io/
      targetRevision: v1.9.0
      helm:
        values: |
          preUpgradeChecker:
            jobEnabled: false
  destination:
    server: https://kubernetes.default.svc
    namespace: longhorn-system
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/addons/ingress-nginx/kustomization.yaml
**chunk:** 1/1

```
resources:
  - application.yaml
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/addons/ingress-nginx/overlays/ingress-grafana.yaml
**chunk:** 1/1

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: grafana
  namespace: observability
  annotations:
    argocd.argoproj.io/sync-wave: "3"
    argocd.argoproj.io/sync-options: SkipDryRunOnMissingResource=true
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
**file:** infra/base/addons/ingress-nginx/overlays/ingress-chat.yaml
**chunk:** 1/1

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: chat-api
  namespace: chat-api
  annotations:
    argocd.argoproj.io/sync-wave: "3"  # После ingress-nginx
    cert-manager.io/cluster-issuer: letsencrypt-dns
    ingress.kubernetes.io/ssl-redirect: "true"
    argocd.argoproj.io/sync-options: SkipDryRunOnMissingResource=true
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - chat.syncjob.ru
      secretName: wildcard-syncjob-tls
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
**file:** infra/base/addons/ingress-nginx/overlays/ingress-argo.yaml
**chunk:** 1/1

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: argocd-server
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "3"
    cert-manager.io/cluster-issuer: letsencrypt-dns
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    argocd.argoproj.io/sync-options: SkipDryRunOnMissingResource=true
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - argo.syncjob.ru
      secretName: argocd-tls
  rules:
    - host: argo.syncjob.ru
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: argocd-server
                port:
                  number: 443
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/addons/ingress-nginx/application.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ingress-nginx
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "1"  # Устанавливается первым
spec:
  project: default
  destination:
    name: CLUSTER  # ← Placeholder, заменится через overlay
    namespace: ingress-nginx
  source:
    repoURL: https://kubernetes.github.io/ingress-nginx
    chart: ingress-nginx
    targetRevision: 4.12.3
    helm:
      values: |
        controller:
          kind: DaemonSet
          ingressClassResource:
            name: nginx
            enabled: true
            default: true
          metrics:
            enabled: true
          admissionWebhooks:
            enabled: true
            timeoutSeconds: 30  # Увеличиваем timeout
            failurePolicy: Ignore
  syncPolicy:
    automated:
      selfHeal: true
      prune: true
    syncOptions:
      - CreateNamespace=true
      - Replace=true  # Для пересоздания проблемных ресурсов
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/addons/cert-manager/kustomization.yaml
**chunk:** 1/1

```
resources:
  - application.yaml
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/addons/cert-manager/cert-cluster.yaml
**chunk:** 1/1

```
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: wildcard-syncjob
  namespace: chat-api
spec:
  secretName: wildcard-syncjob-tls
  dnsNames:
    - "*.syncjob.ru"
    - syncjob.ru
  issuerRef:
    name: letsencrypt-dns
    kind: ClusterIssuer
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/addons/cert-manager/secret-cloudflare-cert-manager-sealed.yaml
**chunk:** 1/1

```
---
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  creationTimestamp: null
  name: cloudflare-api-token
  namespace: cert-manager
spec:
  encryptedData:
    api-token: AgCG/K3uD9ichzmS18vaFNNhWwnz/qU6NqZMSYbljXm1rDXIps2yOwPn3QKQ5DKYp8R0ksHn7lF9OonbWEpJ5M3ADDoDXqSI9Eg8cII+Xdn4Jx56D4K92dPWEYGkwClayCwAVFMBUgY4mzzQKiCDlA5a4eabQ8Nk6bjrrquYXAiWfPSb2S8e+agOstk6a5XDtS7A0FsXv2MBN/qRQk4fZxnKD5+9e0RmQ79YHX7NjRlqSPopCrEt//dP4h5VFMKo/xxicu8YB0xScDVg0DaJy3s+NKnaCMZ+QcNp17z4Dnn3F949/KZfZCJ/Kk33H+1wRcOsriBFbWcuUZXAZoTXEld0kF5ohVfH9uf8EISJEHbcmRupoU4DFRpx+B/D0XTjfcxzSx6mr4rJVcdZoKpwigA63FXgyF2uu0rWoTSW6WAt7SbVheOoklHd4froHgxRW6IGexVE68u+Dd/408CPgAXhdydORd8WLPFssEZeGczH1laogauAeyQp1CvTHW0PHXEsT3a+WZt/TLN95g/fN1gnjEFI8w9X7OSkNY6wZ5WT+Ggy/g9i4betpV/6IZSZNf9xD1uVXj7bhi1m1oy/ODaAI5T+2bV8CvVMbyG30lcTFCx0Ze4SwGG5qRt+MCmdHv4mIUYsCvS+1zvbqo/dZq081f1YwGqCsVGb1PxgYRSHLBGjXwZXVzw35r7i7e5J/8ek+m2iMLdW4cHeSyNg9mq2QyIplkRC4nxde+4I5i95ZRk+GvBt7OCR
  template:
    metadata:
      creationTimestamp: null
      name: cloudflare-api-token
      namespace: cert-manager
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/addons/cert-manager/application.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: cert-manager
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "2"
spec:
  project: default
  destination:
    name: CLUSTER  # ← Placeholder
    namespace: cert-manager
  source:
    repoURL: https://charts.jetstack.io
    chart: cert-manager
    targetRevision: v1.18.0
    helm:
      values: |
        installCRDs: true
        extraArgs:
          - --dns01-recursive-nameservers-only
          - --dns01-recursive-nameservers=8.8.8.8:53,1.1.1.1:53
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/addons/external-dns/kustomization.yaml
**chunk:** 1/1

```
resources:
  - application.yaml
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/addons/external-dns/secret-cloudflare-external-dns-sealed.yaml
**chunk:** 1/1

```
---
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  creationTimestamp: null
  name: cloudflare-api-token
  namespace: external-dns
spec:
  encryptedData:
    api-token: AgA9ZK5bkdusQjGH1IRbr/TNj4V99nTtnKG+iDybRN5ho/tKaHKNUjweqlDWAJtbMFbt3nDq948IDtmajYjmqkhQLKRDG3kgd9FMyEcpJUp4cek0m2LYfGPgvlVBHn2fFVcPHjh9w9toowHW7f/ihYfPZRChQ4og93StXmgxVgj6huHK0AewwxBmeiprsybNdK91lwcZcHB2p7/5oQUjF+LoLil9tlrKzOZPgZMMaK9opAukAUORnYHzQZlFk42SkX+Aj/o79RHZ140mqSe5qDx1gOYUOPc1N8w0lMCNddrTdMiha7VxFaz9QUiqq0UcW4k+nco83PCLppIWivJ1A11yZUMPqwJoWcL5/wgenoecPqPIuyCQz0b1lCW4MgfyqLjHvRLQVAtA7Lrn44QvfdnQkzoXtqBtKtTq6ogON7N3p7XL2sptCl8pOHpC8+H5H8w40h5LuDs1yhbz+vko+kr/A7KhrlTmggQj9h89bP7DJPyeQoIoa7Hh88NW7bqKyl0SSos12ZzIh30h1BxdTF98v8ufIOtwOYtQ88/+d2WD4ihtFxqKZXwI393RiHpleGiXl4XK086isPeqhXYirPvoJ1j0z5Lt2MdL3I2A0AWmMhezzi3CsqwEEYOvrgWrNgcai2975qxuWZvAsR2/TvPG1ExQKlI1cq8Bmnl7yOGYWRC0y1iVsbkVgx96xG1KKESqL5a1KRC2RfSBZJRQDCa107Cs/JYua8VQZp+dh3IlhEV3PcnCcdg+
  template:
    metadata:
      creationTimestamp: null
      name: cloudflare-api-token
      namespace: external-dns
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/addons/external-dns/application.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: external-dns
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "2"
spec:
  project: default
  destination:
    name: CLUSTER  # ← Placeholder
    namespace: external-dns
  source:
    repoURL: https://kubernetes-sigs.github.io/external-dns/
    chart: external-dns
    targetRevision: 1.17.0
    helm:
      values: |
        provider: cloudflare
        sources:
          - ingress
        domainFilters:
          - syncjob.ru
        policy: upsert-only
        logLevel: debug
        env:
          - name: CF_API_TOKEN
            valueFrom:
              secretKeyRef:
                name: cloudflare-api-token
                key: api-token
  syncPolicy:
    automated:
      selfHeal: true
      prune: true
    syncOptions:
      - CreateNamespace=true
```

-------------------------------------------
**role:** config-yaml
**file:** infra/base/crds/app-crds.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: cert-manager-crds
  namespace: argocd
spec:
  destination:
    namespace: cert-manager
    server: https://kubernetes.default.svc
  project: default
  source:
    repoURL: https://github.com/cert-manager/cert-manager.git
    targetRevision: v1.18.0
    path: deploy/crds
  syncPolicy:
    automated:
      selfHeal: true
      prune: true
    syncOptions:
      - CreateNamespace=true
```

-------------------------------------------
**role:** config-yaml
**file:** infra/clusters/prd/kustomization.yaml
**chunk:** 1/1

```
# apiVersion: kustomize.config.k8s.io/v1beta1
# kind: Kustomization

# namePrefix: prd-

# resources:
#   - ../../../base/addons/ingress-nginx
#   - ../../../base/addons/cert-manager
#   - ../../../base/addons/external-dns
#   - ../../../base/addons/observability/loki
#   - ../../../base/addons/observability/grafana
#   - ../../../base/addons/longhorn
#   - ../../../base/services/agent/chat
#   - ../../../base/services/llm/gateway

# # patches:
# #   # Исправляем CLUSTER placeholder для всех Applications
# #   - target:
# #       kind: Application
# #     patch: |-
# #       - op: replace
# #         path: /spec/destination/name
# #         value: prd
# #       - op: replace  
# #         path: /spec/destination/server
# #         value: https://kubernetes.default.svc

# patches:
#   - target:
#       kind: Application
#     patch: |-
#       - op: remove
#         path: /spec/destination/name
#       - op: replace
#         path: /spec/destination/server
#         value: https://kubernetes.default.svc
```

-------------------------------------------
**role:** config-yaml
**file:** infra/clusters/prd/destination.yaml
**chunk:** 1/1

```
# apiVersion: argoproj.io/v1alpha1
# kind: Application
# metadata:
#   name: all                    # имя здесь неважно – патч применится по kind
# spec:
#   destination:
#     name: prd                  # ТОЧНОЕ имя prod-кластера из `argocd cluster list`
#     namespace: argocd          # можно опустить, если в base уже указано
```

-------------------------------------------
**role:** config-yaml
**file:** infra/clusters/dev/kustomization.yaml
**chunk:** 1/1

```
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namePrefix: dev-
resources:
  - ../../base/addons/ingress-nginx
  - ../../base/addons/cert-manager
  - ../../base/addons/external-dns
  - ../../base/addons/observability/loki
  - ../../base/addons/observability/grafana
  - ../../base/services/agent/chat
  - ../../base/services/llm/gateway

patches:
  - path: destination.yaml
    target:
      kind: Application
```

-------------------------------------------
**role:** config-yaml
**file:** infra/clusters/dev/destination.yaml
**chunk:** 1/1

```
# infra/clusters/dev/destination.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: all
  namespace: argocd
spec:
  project: default
  destination:
    server: https://kubernetes.default.svc
```

-------------------------------------------
**role:** config-yaml
**file:** infra/_roles/prd.yaml
**chunk:** 1/1

```
# apiVersion: argoproj.io/v1alpha1
# kind: Application
# metadata:
#   name: prd-app                                # любое уникальное имя
#   namespace: argocd
#   labels:
#     tier: argocd
#   finalizers:
#     - resources-finalizer.argocd.argoproj.io
# spec:
#   destination:
#     name: prd                                # <= имя prd-кластера в Argo CD
#     namespace: argocd
#   project: default
#   source:
#     repoURL: https://github.com/justgithubaccount/app-release.git
#     path: infra/clusters/prd                      # overlay-директория этого кластера
#     targetRevision: main
#   syncPolicy:
#     automated:
#       allowEmpty: true
#       selfHeal: true
#       prune: true
#     syncOptions:
#       - Validate=true
#       - CreateNamespace=true
#       - PruneLast=true
```

-------------------------------------------
**role:** config-yaml
**file:** infra/_roles/dev.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: dev-app                                  # любое уникальное имя
  namespace: argocd
  labels:
    tier: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  destination:
    name: dev                                # <= имя dev-кластера в Argo CD
    namespace: argocd
  project: default
  source:
    repoURL: https://github.com/justgithubaccount/app-release.git
    path: infra/clusters/dev                      # overlay-директория этого кластера
    targetRevision: main
  syncPolicy:
    automated:
      allowEmpty: true
      selfHeal: true
      prune: true
    syncOptions:
      - Validate=true
      - CreateNamespace=true
      - PruneLast=true
```

