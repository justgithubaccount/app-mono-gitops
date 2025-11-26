> Все таки нужно сразу [?] было делать мульти-репо. Проект ушел в архив. Будет разделен на 3+ (сервис на питоне/хелм-обертки под сервисы/k8s-gitops-deploy...)

# 🧠 Bio AI Agent Infrastructure

> Идет отладка - 95% (tst, dev) | 65% (stg) | prd (20%)  

> Next Up - DevOps Copilot (по большой части можно на основе OpenWebUI сделать Copilot подключив к нему АPI сервисов и MCP для сервисов)  

> Проект временно остановлен, все дампы памяти расписанны ниже в [Content](https://github.com/justgithubaccount/app-mono-gitops?tab=readme-ov-file#-%D1%81ontent-main)-секциях  
> Дальньшая разработка начнется с добавления KeyClock, рефакторинга текущий структуры в `infra/` под [GitOps платформу](https://github.com/justgithubaccount/app-mono-gitops/pulls)...  
> И самое важное гармонично вплести [Backstage](https://github.com/backstage/backstage) + mesh (истио или линкерд, еще какой-то там был более-менее), и получить протатип cncf-gitops стека на 2025+  год + kaniko закрыт, форкнут, как то там оно счет иб, не понятно, особенно в связке с mtls  

## Getting Started (Clear Install)

Установить в новый кластер с нуля с восстановлением всех ресов кластера на основе роли (секреты нужно обновить и пару синков запустить)  

```bash
kubectl create namespace argocd  
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.0.12/manifests/ha/install.yaml  
git clone https://github.com/justgithubaccount/app-release.git  
cd app-release  
kubectl apply -f infra/roles/role-dev-enviroment.yaml  
```

Поднимется API на FastAPI, будут проброшенны вэбки для Argo, Grafana через CloudFlare (ssl + dns), Longhorn. 
Приложение будет слать логи в Vector (OTLP Exporter) на основе OpenTelemtry в Loki + еще что-то по мелочи, в целом в манифестах можно глянуть подробнее

> https://argo.syncjob.ru/  
> https://grafana.syncjob.ru/  
> https://chat.syncjob.ru/  

## About System  
Хотелось просто что-то такого что мне поможет в моей же работе, по принципу "единого окна" в каком-нибудь крупном энтерпрайзе, что все материалы которые у меня скопились за всю жизнь (текст, видео, статьи, ну кароче данные), станут доступны просто по запросу на уровне "погуглить", только в контекте ИИ  

Изначально все родилось с идеи создать микро-сервисную архитектуру для ии-агента с подключеним CrewAI, но перед этим еще нужно было потестить эко-систему от Арго  

В `apps/` живут сервисы, отвечающие за логические сущности ии-агента и в целом системы  
В `charts/` соответственно хелм-обертки под эти сервисы  
В `infra/base/services` соответственно эти сервисы обернуты в `kind` типа `Application`  

После применения `infra/roles/role-dev-enviroment.yaml` подхватывается overlay `infra/clusters/dev/kustomization.yaml` для этой роли (можно воспринимать как разрешение, т.е. что будет установленно в кластер), в котором можно посмотреть что будет применно к этому кластеру  

Благодаря GitOps все крайне прозрачно и предусматривает управление любым кол-вом кластеров 100+ 

---

По хорошему Арго должен жить в отдельном кластере  
Репа изначально задумывалсь как моно-репа, с возможность разбития (но, на начальном этапе в этом нет смысла), тот же хелм-релиз это две репы, одна под темлейты, другая под вальюсы...  

---

[CrewAI](https://github.com/justgithubaccount/app-crewai-cluster) живет в отдельной репе и в сути идея чтобы на него вынести всю рутину от адмиства/девопса/sre до залива в сторы и прочие, т.е. делигировать его о во все слои процессы разработки и бизнес составялющией. Благодаря этому будет достигнута большая прозрачность и автомазация + буст к ускорению всех процессов...  

---

Сам агент будет жить в другой репе, реализация на [Dify](https://dify.ai/), CrewAI будет передавать ему контекст от системы. В Dify есть встроенная вэбка, но будет отдельный интерфейс для "разговора со всеми элементами системы" на базе [open-webui](https://github.com/open-webui/open-webui). Хотя проще сразу делать свой фронт...

## About GitOps  

GitOps составляющая взята из подкаста [DKT66 - Что такое GitOps и с чего начать?](https://www.youtube.com/watch?v=5ljFkYqWN4c) + [репа так сказать к подкасту](https://github.com/devOwlish/argocd-demo) (в моем понимание ценности этой инфы нет предела)  

[DKT80 - Интервью с автором ArgoCD](https://www.youtube.com/watch?v=BCer7ybcb1Y) просто создатель Арго рассказывает как все начиналось и зачем было задуманно. У ребят было 5к кодеров которым нужно было дать лаконичный инструмент для работы с кубиком. Вэбка зарешала. ~~GitOps просто маркетинг не более~~  

Логика ролевой системы для GitOps будет строится на моем прошлом опыте работы и архитектуры Active Directory (ну как ее строят в real-enterprise-shit). В целом так делать не надо ([есть рабочий паттерн](misc/context/gitops/gitops-platform.md)), но интересно куда это приведет...

## 📄 Сontent (main)
 - ⏳ [Таски проекта](misc/README-tasks.md)   
 - ℹ️ [Disclaimer](misc/README-disclaimer.md)  
 - 🌱 [Consept](misc/README-consept.md)  
 - 🧪 [Why Bio?](misc/context/how-to-bio.md)  
 - 🗂️ [Old README](misc/README-old.md)  

## 📄 Сontent (ops)
 - 🌐 [GitOps Multi Cluster](/misc/multi-cluster.yaml)  
 - 🐙 [GitOps Basis](/misc/context/gitops/)  
 - 🐳 [K8s Basis](/misc/context/k8s/)  
 - 🔖 [SemVer + Conventional Commits](/misc/context/git/)  
 - 🔄 [All Layers of CI](/misc/context/ci/)  

## 📄 Сontent (code) (немножко устарело)
- 🧠 [Архитектура классов chat-api](misc/context/chat-api-classes.md)
- ⚙️ [Использование OpenTelemetry](misc/context/open-telemetry.md)
- 🤖 [Определения CrewAI и поведение агентов](misc/context/crewai-definition.md)
- 📜 [Общий обзор CrewAI](misc/context/crewai-general.md)
- 🛠️ [Примеры задач для Codex](misc/context/codex-task-example.md)
