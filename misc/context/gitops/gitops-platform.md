> Приимерный пример, чтобы в голове не держать  

Cейчас структура такая:

```
infra/
  base/
    addons/
    crds/
    services/
  clusters/
    dev/
    prd/
    github/
  roles/
    role-dev-enviroment.yaml
    role-prd-enviroment.yaml
  infra-root.yaml
```

Если сравнивать с «правильным» GitOps-паттерном, то различия такие:

### Как обычно делают

```
infra/
  platform/               # общий слой (ингресс, cert-manager, dns, observability, secrets, automation)
    networking/
    security/
    observability/
    argocd/
    automation/

  clusters/               # конкретные окружения
    dev/
      kustomization.yaml
      app-of-apps.yaml    # маленький bootstrap, тянет platform
    prd/
      kustomization.yaml
      app-of-apps.yaml

  apps/                   # приложения
    chat-api/
      base/
      overlays/
        dev/
        prd/
```

### Что у тебя сейчас

* Папка **roles/** фактически заменяет концепцию `platform/` → туда свалено всё, что связано с окружениями.
* В **base/** лежат сервисы/аддоны, но без чёткой привязки к тому, это часть платформы или приложения.
* В **clusters/** кроме dev/prd у тебя ещё `github/` — похоже, это эксперимент с настройками?

### Главное отличие

Правильнее, чтобы **roles/** стало **platform/**.

* Там будут системные вещи, одинаковые для всех кластеров.
* В кластерах (`clusters/dev` и `clusters/prd`) остаётся только App-of-Apps, который ссылается на `platform/`.
