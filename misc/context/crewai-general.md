Вот полное `README.md`, структурированное по документации **CrewAI** (включая Strategy, Agents, Crews, Flows и Advanced). Это основа для твоего проекта на базе `CrewAI`, понятная другим разработчикам или CI/CD-системам:

---

# 🤖 CrewAI Agent System

> Production-ready agent orchestration with structured roles, flows, and observability.

---

## 📌 Overview

This repository implements an **AI-agent microservice** powered by [CrewAI](https://docs.crewai.com), built on top of **FastAPI**, supporting YAML-based configurations for roles, tasks, and flows. Agents operate within a Crew, executing workflows, analyzing results, and adapting via Notion or local files.

---

## 🧭 Strategy

CrewAI is used to manage infrastructure as **an evolving organism**.

### ✅ Use Cases

* Declarative agent orchestration via YAML
* GitOps/LLMOps coordination (e.g., deployments, issue triage)
* Monitoring (logs, metrics, patterns) with LLM post-analysis
* Infrastructure-as-context: crew memory = repo history + logs

---

## 🧠 Agents

### 🏷 What is an Agent?

An **Agent** is a persona with:

| Attribute   | Description                               |
| ----------- | ----------------------------------------- |
| `role`      | Defines their identity and capabilities   |
| `goal`      | Mission or objective                      |
| `tools`     | Allowed tools (e.g. `kubectl`, `httpx`)   |
| `tasks`     | Executable plans                          |
| `memory`    | Long-term or short-term knowledge context |
| `backstory` | Optional narrative to guide behavior      |

Example:

```yaml
- id: incident_llm_analyst
  name: Incident LLM Analyst
  goal: Analyze logs and raise GitHub issues.
  tools: [Loki, Prometheus, GitHub API]
  memory: [loki_queries.md, past_issues.yaml]
  context: MCP agent connected to observability streams
```

---

## 👥 Crews

### 🤝 What is a Crew?

A **Crew** is a group of agents working together to solve tasks via a **process** (e.g. sequential, hierarchical).

Example `crew.yaml`:

```yaml
crew_name: infra-cluster-intelligence
description: >
  This Crew manages GitOps deployments, log analysis,
  and the evolution of AI-agent architecture.

roles:
  - id: deployment_arbiter
    name: GitOps Arbiter
    goal: Ensure clean declarative deployments using Flux
    tools: [fluxctl, kustomize]
    memory: [git_history.md]
```

You can load and run:

```python
from crewai import Crew
crew = Crew.load("infra-cluster.yaml")
crew.kickoff()
```

---

## 🔄 Flows

Flows define the **execution pattern** of tasks across agents.

### 🚧 Flow Types:

| Type           | Description                                 |
| -------------- | ------------------------------------------- |
| `sequential`   | Tasks are executed in order                 |
| `hierarchical` | Managers assign tasks to agents dynamically |
| `conditional`  | Tasks branch based on outcomes              |

Use in YAML:

```yaml
process: sequential
```

Each task in a flow can specify:

```yaml
- description: Fix out-of-sync apps in ArgoCD
  expected_output: PR with changes
  agent: deployment_arbiter
```

---

## 🔐 Advanced

### 🧬 Customizing Prompts

Prompts can be customized at 3 levels:

1. **Task level** (`task.prompt`)
2. **Agent level** (`agent.backstory`, `agent.goal`)
3. **Crew template** (global prompt template)

Supports templating with:

```python
task.prompt.format(agent=agent, memory=memory)
```

Use Jinja2-like variables in YAML:

```yaml
description: Investigate logs
context:
  - "Use memory: {{ memory.logs }}"
  - "Be concise and precise"
```

---

### 🧷 Fingerprinting (Unique Crew Identity)

Each Crew can be fingerprinted based on:

* Crew name and purpose
* YAML hash (e.g. Git SHA)
* Agent composition

Use this for reproducibility, logging, or versioning:

```python
crew.fingerprint()  # returns unique ID
```

---

## 🧪 Testing

Make sure tests run in the correct environment:

```bash
make test
```

Include `pytest`, `httpx`, `fastapi` in `dev-dependencies` (`pyproject.toml`):

```toml
[project.optional-dependencies]
dev = [
  "pytest",
  "httpx",
  "fastapi",
  "pytest-asyncio"
]
```

---

## 📂 Project Structure

```
apps/
  chat/
    app/
      main.py
      behavior/
      integrations/
      services/
    crew-infra-cluster.yaml
    tests/
manifests/
  chat-api-deployment.yaml
  chat-api-service.yaml
docs/
  README.agents.md
  README.flows.md
  README.prompting.md
pyproject.toml
Makefile
```

---

## ✅ CI & Deployment

* GitHub Actions builds Docker image on push to `main`
* ArgoCD tracks `manifests/` for GitOps-style sync
* Notion config and agent behavior can be loaded at runtime

---

Если хочешь, могу:

* Сгенерировать все `README.*.md` по секциям
* Создать `crew-infra-cluster.yaml` на основе структуры выше
* Добавить Makefile с `test`, `run`, `lint` командами

Хочешь?
