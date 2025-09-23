# 🧠 Bio AI Agent Infrastructure

> Идет отладка - 95% (tst, dev)  
> Next Up - DevOps Copilot  

## Getting Started (Clear Install)

Установить в новый кластер с нуля с восстановлением всех ресов кластера на основе роли (секреты нужно обновить и пару синков запустить)  

```bash
kubectl create namespace argocd  
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.0.12/manifests/ha/install.yaml  
git clone https://github.com/justgithubaccount/app-release.git  
cd app-release  
kubectl apply -f infra/roles/role-dev-enviroment.yaml  
```

GitOps составляющая взята из подкаста [DKT66 - Что такое GitOps и с чего начать?](https://www.youtube.com/watch?v=5ljFkYqWN4c) + [репа так сказать к подкасту](https://github.com/devOwlish/argocd-demo) (в моем понимание ценности этой инфы нет предела)  

[DKT80 - Интервью с автором ArgoCD](https://www.youtube.com/watch?v=BCer7ybcb1Y) просто создатель Арго рассказывает как все начиналось и зачем было задуманно. У ребят было 5к кодеров которым нужно было дать лаконичный инструмент для работы с кубиком. Вэбка зарешала. ~~GitOps просто маркетинг не более~~  

Логика ролевой системы для GitOps будет строится на моем прошлом опыте работы и архитектуры Active Directory (ну как ее строят в real-enterprise-shit). В целом так делать не надо (есть рабочий паттерн), но интересно куда это приведет

## 📄 Содержание
- 🧠 [Архитектура классов chat-api](misc/context/chat-api-classes.md)
- ⚙️ [Использование OpenTelemetry](misc/context/open-telemetry.md)
- 🤖 [Определения CrewAI и поведение агентов](misc/context/crewai-definition.md)
- 📜 [Общий обзор CrewAI](misc/context/crewai-general.md)
- 🛠️ [Примеры задач для Codex](misc/context/codex-task-example.md)
