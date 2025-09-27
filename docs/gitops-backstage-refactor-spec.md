# GitOps Platform Refactor and Backstage Enablement Technical Specification

## 1. Purpose
This specification describes the changes required to reorganize the repository into a domain-oriented GitOps layout and to introduce Backstage (Red Hat Developer Hub chart) as part of the internal developer platform. The desired end state keeps all cluster configuration in Git, delivers it through Argo CD, and exposes observability and platform capabilities through Backstage.

## 2. Scope
- Migrate the current `roles/` content into a new `infra/platform/` hierarchy that separates concerns by domain.
- Define Argo CD AppProjects (`platform`, `apps`) and per-environment App-of-Apps bootstraps for `dev` and `prd` clusters.
- Model Argo CD Applications for platform services: Backstage, Vector Gateway, ingress, cert-manager, External Secrets, and the observability stack (Loki, Tempo, Prometheus, Grafana).
- Store Helm values beneath `infra/platform/values/<component>/` with base overlays and environment-specific overrides.
- Install Backstage via the Red Hat Developer Hub Helm chart, including baseline app-config (proxying Grafana/Prometheus/Tempo), required plugins, and Kubernetes integration.
- Configure Backstage access to Kubernetes (service account with `backstage.io/kubernetes-id` labels/annotations on workloads).
- Manage platform secrets using External Secrets (Backstage database password, Grafana tokens, etc.).
- Provide CI validation for manifests (Helm lint/template, kubeconform, OPA policy checks).
- Deliver documentation covering repository structure, pipelines, rollback strategy, and SLA/SoP references.

## 3. Out of Scope
- Rewriting application charts or redesigning workloads beyond structural reorganization and Backstage onboarding.
- Data migrations—Backstage connects to the existing Postgres (Patroni/PgBouncer) deployment only.

## 4. Target Repository Layout
```
infra/
  base/
    addons/
    crds/
    services/
  platform/
    apps/
      backstage-application.yaml
      vector-gateway-application.yaml
      ingress-application.yaml
      cert-manager-application.yaml
      external-secrets-application.yaml
      observability-application.yaml
    values/
      backstage/
        base.yaml
        dev.yaml
        prd.yaml
      vector/
        base.yaml
        dev.yaml
        prd.yaml
    kustomization.yaml
  clusters/
    dev/
      app-of-apps.yaml
      kustomization.yaml
    prd/
      app-of-apps.yaml
      kustomization.yaml
  projects/
    argocd-project-platform.yaml
    argocd-project-apps.yaml
  infra-root.yaml

apps/
  chat-api/
    chart/
    values/
      values-dev.yaml
      values-prd.yaml
catalog/
  chat-api/catalog-info.yaml
```

## 5. Argo CD Configuration
### 5.1 AppProjects
- `infra/projects/argocd-project-platform.yaml`: defines the platform project with access to required namespaces and source repositories (GitHub repo, RHDH chart repo, optional external charts).
- `infra/projects/argocd-project-apps.yaml`: defines the apps project with wildcard namespace access for application teams.

### 5.2 Environment Bootstrapping
- `infra/clusters/dev/app-of-apps.yaml` and `infra/clusters/prd/app-of-apps.yaml` bootstrap the platform by syncing `infra/platform/apps` using automated pruning and self-healing. Each environment pins its desired Git revision.

### 5.3 Platform Applications
- Each file under `infra/platform/apps/` declares an Argo CD Application pointing to the relevant chart or manifest path, uses environment overlays via `valueFiles`, enables `CreateNamespace`, and sets automated sync with self-heal/prune.

## 6. Backstage Deployment
- Source the Backstage chart from `https://redhat-developer.github.io/rhdh-chart`, pinning the chosen version.
- Helm values in `infra/platform/values/backstage/` configure:
  - `backstage.appConfig` including portal title, base URL, and reverse proxies for Grafana, Prometheus, and Tempo APIs.
  - Ingress with TLS for `https://backstage.<environment-domain>/`.
  - Dynamic plugin enablement (Kubernetes, Grafana, Prometheus, optional Jaeger).
  - External Postgres connection details (host, port, database, user).
  - Resource requests/limits and ServiceMonitor settings for metrics scraping.
- Use External Secrets to source sensitive data (DB password, API tokens) into Kubernetes secrets consumed by the chart.
- Ensure Backstage’s Kubernetes plugin can discover workloads via `backstage.io/kubernetes-id` labels on Deployments/Pods and the linked Backstage entity metadata.

## 7. Observability and Telemetry
- Deploy Vector Gateway as an OTLP aggregator that forwards logs to Loki, traces to Tempo, and metrics to Prometheus while exposing a Prometheus metrics endpoint.
- Maintain consistent Loki labels (`service_name`, `namespace`, `app.kubernetes.io/name`) and keep trace identifiers as log fields.
- Provide Grafana dashboards and Tempo/Prometheus endpoints that Backstage proxies for unified visibility.
- Enforce PodSecurity and NetworkPolicies (default deny with explicit allowances between services and data stores).

## 8. External Secrets Strategy
- Reference a ClusterSecretStore (e.g., Consul/Vault) for all sensitive values.
- Define ExternalSecret manifests (e.g., `backstage-db-password`) to materialize secrets in target namespaces with structured templates.
- Avoid committing plaintext secrets to the repository; rely solely on External Secrets reconciliation.

## 9. CI/CD and Policy Controls
- Establish GitHub Actions (or equivalent) that run on every change:
  - `helm lint` and `helm template` for all charts and overlays.
  - `kubeconform` against rendered manifests.
  - Policy enforcement through Kyverno or Gatekeeper (ensuring security context, mandatory labels, no inline secrets).
  - Optional quality checks (`yamllint`, `ruff`, `prettier`).
- Adopt conventional commits and semantic-release workflows for traceable change management.

## 10. Acceptance Criteria
1. Platform structure matches the target layout with all platform Applications under `infra/platform/*` and bootstrap files under `infra/clusters/<env>/`.
2. AppProjects constrain platform and app deployments to approved namespaces and source repositories.
3. Backstage Application is healthy in Argo CD and publicly reachable with TLS, exposing Kubernetes, Prometheus, and Grafana integrations for services like `chat-api`.
4. Vector Gateway reliably receives OTLP traffic and fans out to Loki/Tempo/Prometheus, enabling trace-to-log workflows via Grafana.
5. Secrets for Backstage and platform integrations are sourced exclusively through External Secrets; no sensitive values are committed to Git.
6. CI pipelines covering Helm rendering, schema validation, and policy enforcement complete successfully.

## 11. Migration Plan
1. Create a feature branch (e.g., `refactor/platform-layer`).
2. Relocate `roles/` content into the new platform hierarchy and introduce values overlays.
3. Add AppProjects and environment App-of-Apps manifests.
4. Bootstrap the `dev` environment with the new structure and validate component health.
5. Configure Backstage connectivity to the external Postgres instance and verify plugin functionality.
6. Register application entities (e.g., `catalog/chat-api/catalog-info.yaml`) and annotate Kubernetes workloads for Backstage discovery.
7. After successful validation, promote the changes to `prd` via GitOps (merge and synchronize).

## 12. Documentation Deliverables
- Update the repository README to reference the new layout and Backstage entry point.
- Provide runbooks describing deployment, rollback, and incident response procedures.
- Document SLA/SLO expectations for the platform stack (Backstage, observability components, External Secrets controller).

