# kubeseal
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.32.2/kubeseal-0.32.2-linux-amd64.tar.gz
tar -xvzf kubeseal-0.32.2-linux-amd64.tar.gz
sudo install -m 755 kubeseal /usr/local/bin/kubeseal

### Chat Application

# OpenRouter
kubectl create secret generic chat-openrouter \
  --from-literal=OPENROUTER_API_KEY="sk-or-v1-30895..." \
  --namespace=chat-api \
  --dry-run=client -o json | \
kubeseal --controller-name=sealed-secrets --controller-namespace=kube-system \
  --format yaml > infra/base/services/agent/chat/openrouter-secrets.yaml  

# DB
kubectl create secret generic chat-postgree \
  --from-literal=DATABASE_URL="postgresql://gen_user:********@192.168.0.6:5432/chat-api" \
  --namespace=chat-api \
  --dry-run=client -o json | \
kubeseal --controller-name=sealed-secrets --controller-namespace=kube-system \
  --format yaml > infra/base/services/agent/chat/postgree-secrets.yaml

# GitHub (argo-image-updater)
kubectl create secret generic chat-github  \
  --from-literal=GITHUB_TOKEN="ghp_pa8ow..." \
  --namespace=argocd \
  --dry-run=client -o json | \
kubeseal --controller-name=sealed-secrets --controller-namespace=kube-system \
  --format yaml > infra/base/services/agent/chat/github-secrets.yaml

# True Creds for Argo Image Updater
kubectl create secret generic chat-github \
  --namespace=argocd \
  --from-literal=url=https://github.com/justgithubaccount/app-release \
  --from-literal=username=justgithubaccount \
  --from-literal=password=ghp_PpwlZ... \
  --dry-run=client -o json | \
jq '.metadata.labels["argocd.argoproj.io/secret-type"]="repository"' | \
kubeseal --controller-name=sealed-secrets \
  --controller-namespace=kube-system \
  --format yaml > infra/base/services/agent/chat/github-secrets.yaml

### Auto certs with dns (same token)

# Certmanager
kubectl create secret generic cert-manager-secret  \
  --from-literal=CLOUDFLARE_TOKEN="PPVVv..." \
  --namespace=cert-manager \
  --dry-run=client -o json | \
kubeseal --controller-name=sealed-secrets --controller-namespace=kube-system \
  --format yaml > infra/base/addons/cert-manager/cloudflare-secrets.yaml

# Cloudflare
kubectl create secret generic external-dns-secret  \
  --from-literal=CLOUDFLARE_TOKEN="PPVVv..." \
  --namespace=external-dns \
  --dry-run=client -o json | \
kubeseal --controller-name=sealed-secrets --controller-namespace=kube-system \
  --format yaml > infra/base/addons/external-dns/cloudflare-secrets.yaml
