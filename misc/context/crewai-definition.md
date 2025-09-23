Вот полный набор YAML-структур для описания **поведения агентов** и **архитектуры CrewAI**, основанный на лучших практиках и документации CrewAI. Они делятся на три уровня:

---

## 🧠 1. **Behavior Definition (agent tasks + crew logic)**

Обычно берётся из **Notion** (или лежит в YAML-файле, например `behavior.yaml`):

```yaml
process: sequential  # или "reactive", "manual"
agents:
  - role: infra_senior_pairing_agent
    goal: Maintain cluster architecture and observability in Git.
    backstory: Senior DevOps engineer working in tandem.
    tools: [kubectl, terraform, fluxctl, clickhouse-client]
    allow_delegation: true
    tasks:
      - description: Analyze recent changes in cluster manifests.
        expected_output: Summary of drift and needed sync.
        context: ["Focus on workloads and secrets."]
        agent: infra_senior_pairing_agent

  - role: incident_llm_analyst
    goal: Investigate logs and raise GitHub issues.
    tools: [Loki, Prometheus, OpenAI API]
    allow_delegation: false
    tasks:
      - description: Scan logs for anomalies
        context: ["Use Loki query templates from knowledge base."]
        expected_output: Root-cause summary + recommended actions
```

---

## ⚙️ 2. **Crew Definition (High-level system)**

YAML-файл для загрузки через `Crew.load("crew.yaml")`:

```yaml
crew_name: infra-cluster-intelligence
description: >
  Manages infrastructure ops, observability, GitOps and bio-infra.

agents:
  - id: infra_senior_pairing_agent
    name: Senior Infra Engineer (Pairing Agent)
    goal: Maintain cluster architecture and observability in Git.
    tools: [kubectl, terraform, fluxctl, clickhouse-client]
    memory: cluster manifests, observability history
    context: dual setup with another senior

  - id: deployment_arbiter
    name: GitOps Arbiter
    goal: Declarative deployments via FluxCD
    tools: [fluxctl, kustomize, helm, git]
    memory: Git history, Helm charts
    context: watches for drift, auto-reverts failures

  - id: ecosystem_engineer
    name: Ecosystem Architect
    goal: Architect agent protocol as evolving system
    tools: [graphviz, langchain, crewai-cli]
    memory: architecture history, diagrams
    context: genome = repo, agents = living organs

process: sequential
entry_point: ecosystem_engineer
```

---

## 🧩 3. **Flow Definition (multi-step LLM plan)**

Если ты хочешь задать **шаги обработки**, можно использовать:

```yaml
flow_name: log-triage-pipeline
description: >
  From log ingestion to root cause analysis and ticket creation.

steps:
  - id: gather_logs
    agent: incident_llm_analyst
    description: Query logs from Loki with given pattern
    inputs: ["pattern: level=error"]
    output: "logs.json"

  - id: detect_anomalies
    agent: incident_llm_analyst
    description: Use LLM to analyze logs for anomalies
    inputs: ["logs.json"]
    output: "summary.md"

  - id: create_issue
    agent: deployment_arbiter
    description: Create GitHub issue with root cause
    inputs: ["summary.md"]
    output: "issue_url"
```

---

## ✅ Рекомендации

| Вид            | YAML-файл                    | Назначение                              |
| -------------- | ---------------------------- | --------------------------------------- |
| Поведение      | `behavior.yaml` (или Notion) | Инструкция агентам, как действовать     |
| Команда (Crew) | `crew-infra-cluster.yaml`    | Архитектура агентов, кто с кем работает |
| Flow           | `flow-log-analysis.yaml`     | Пошаговый сценарий работы агентов       |

---

Хочешь — могу сразу сгенерировать `crew-infra-cluster.yaml` под твой проект (или перевести Notion YAML в нужный формат).
