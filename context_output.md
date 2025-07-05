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
**file:** infra/clusters/prd/kustomization.yaml
**chunk:** 1/1

```
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namePrefix: prd-

resources:
  - ../../../base/addons/ingress-nginx
  - ../../../base/addons/cert-manager
  - ../../../base/addons/external-dns
  - ../../../base/addons/observability/loki
  - ../../../base/addons/observability/grafana
  - ../../../base/addons/longhorn
  - ../../../base/services/agent/chat
  - ../../../base/services/llm/gateway

patches:
  # Исправляем CLUSTER placeholder для всех Applications
  - target:
      kind: Application
    patch: |-
      - op: replace
        path: /spec/destination/name
        value: prd
      - op: replace  
        path: /spec/destination/server
        value: https://kubernetes.default.svc
```

-------------------------------------------
**role:** config-yaml
**file:** infra/clusters/prd/destination.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: all                    # имя здесь неважно – патч применится по kind
spec:
  destination:
    name: prd                  # ТОЧНОЕ имя prod-кластера из `argocd cluster list`
    namespace: argocd          # можно опустить, если в base уже указано
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
  - ../../../base/addons/ingress-nginx
  - ../../../base/addons/cert-manager
  - ../../../base/addons/external-dns
  - ../../../base/addons/observability/loki
  - ../../../base/addons/observability/grafana
  - ../../../base/services/agent/chat
  - ../../../base/services/llm/gateway

patches:
  # Исправляем CLUSTER placeholder для всех Applications
  - target:
      kind: Application
    patch: |-
      - op: replace
        path: /spec/destination/name
        value: dev
      - op: replace
        path: /spec/destination/server  
        value: https://kubernetes.default.svc
```

-------------------------------------------
**role:** config-yaml
**file:** infra/clusters/dev/destination.yaml
**chunk:** 1/1

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: all                    # имя здесь неважно – патч применится по kind
spec:
  destination:
    name: dev                  # ТОЧНОЕ имя prod-кластера из `argocd cluster list`
    namespace: argocd          # можно опустить, если в base уже указано
```

