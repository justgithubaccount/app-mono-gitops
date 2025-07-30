package kubernetes

default deny = []

# 🛡️ 1. Контейнеры должны иметь ресурсы
deny[msg] {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  not container.resources.limits.memory
  msg := sprintf("Container %s missing memory limit", [container.name])
}

deny[msg] {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  not container.resources.limits.cpu
  msg := sprintf("Container %s missing CPU limit", [container.name])
}

# 🔬 2. Должны быть probes
deny[msg] {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  not container.livenessProbe
  msg := sprintf("Container %s missing livenessProbe", [container.name])
}

deny[msg] {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  not container.readinessProbe
  msg := sprintf("Container %s missing readinessProbe", [container.name])
}

# 📛 3. Namespace должен быть указан
deny[msg] {
  not input.metadata.namespace
  msg := "Resource is missing namespace"
}

# 🔐 4. Контейнеры должны запускаться не от root
deny[msg] {
  input.kind == "Deployment"
  not input.spec.template.spec.securityContext.runAsNonRoot
  msg := "Deployment must set runAsNonRoot: true"
}

# 📦 5. Если используется LLM — должна быть задана модель
deny[msg] {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  input.metadata.labels["app.kubernetes.io/name"] == "chat-api"
  not input.spec.template.metadata.annotations["openrouter.model"]
  msg := "chat-api is missing openrouter.model annotation"
}

# 🔭 6. OTEL переменные должны быть заданы
deny[msg] {
  input.kind == "Deployment"
  container := input.spec.template.spec.containers[_]
  not container.env[_].name == "OTEL_EXPORTER_OTLP_ENDPOINT"
  msg := "OpenTelemetry OTLP endpoint is missing"
}
