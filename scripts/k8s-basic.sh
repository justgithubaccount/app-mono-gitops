#!/bin/bash
set -euo pipefail

### ===========================================
### 💡 NAMESPACE CONTEXT — define your workload
### ===========================================
# This is the namespace where your application (e.g. chat-api) lives.
# Change it to switch context across environments (dev, staging, prod).
NS="chat-api"

### ===============================
### 🧠 KUBECONFIG — Select a cluster
### ===============================
# Sets the kubeconfig context to connect to a specific cluster
export KUBECONFIG=/home/jenya/kube/twc-reasonable-umbriel-config.yaml
# export KUBECONFIG=/home/jenya/kube/twc-brainy-plover-config.yaml

echo "[1] ✅ KUBECONFIG set to $KUBECONFIG"

### ==================================
### 🚀 INITIAL SETUP — ArgoCD + Ingress + Sealed Secrets
### ==================================
# ArgoCD: GitOps controller
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# ingress-nginx: HTTP entry point into cluster
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.12.2/deploy/static/provider/cloud/deploy.yaml

# Sealed Secrets controller — encrypt secrets for Git
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/latest/download/controller.yaml

echo "[2] ✅ Core GitOps stack deployed (ArgoCD + Ingress + SealedSecrets)"

### ================================
### 🔐 Port-forward + Argo login
### ================================
echo "[3] 🔐 ArgoCD web UI on http://localhost:8080"
kubectl port-forward svc/argocd-server -n argocd 8080:443 &
sleep 3

echo "[🔑 ArgoCD admin password:]"
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
echo

### ================================
### 📦 GitOps deployment (custom app)
### ================================
# Apply ArgoCD Application resource from Git
kubectl apply -f app.yaml
echo "[4] 📦 ArgoCD Application applied: app.yaml"

### ================================
### 🔐 Sealing secrets (before Git)
### ================================
# Convert Kubernetes Secrets to encrypted SealedSecrets
kubectl create -f litellm-secrets.yaml --dry-run=client -o json | kubeseal --format yaml > litellm-secrets-sealed.yaml
kubectl create -f chat-api-secrets.yaml --dry-run=client -o json | kubeseal --format yaml > chat-api-secrets-sealed.yaml
echo "[5] 🔐 SealedSecrets generated"

### ================================
### 📊 Basic diagnostics per namespace
### ================================
echo "[6] 📊 Resources in namespace: $NS"
kubectl get pods -n $NS
kubectl get svc -n $NS
kubectl get deployment -n $NS
kubectl get configmap -n $NS
kubectl get secret -n $NS
kubectl get ingress -n $NS

# NGINX Ingress controller status
kubectl get svc -n ingress-nginx

### ================================
### 🔄 Rollout + Debug actions
### ================================
# Restart Deployment (forces rollout of new pods)
kubectl rollout restart deployment chat-api -n $NS

# Delete Pods by label (forces re-creation)
kubectl delete pod -n $NS -l app=litellm
kubectl delete pod -n $NS -l app=chat-api

# Logs for litellm (last 50 lines)
kubectl logs -n $NS -l app=litellm | tail -n 50

# Get image used by deployment
kubectl get deploy -n $NS chat-api -o=jsonpath="{.spec.template.spec.containers[0].image}"
echo
kubectl get pods -n $NS -o jsonpath='{.items[*].spec.containers[*].image}'
echo

### ================================
### 🧪 Exec inside container
### ================================
# Run debugging command inside running pod
kubectl exec -n $NS -it $(kubectl get pod -n $NS -l app=litellm -o jsonpath='{.items[0].metadata.name}') \
  -- litellm --config /app/config.yaml --detailed_debug

# Print environment of litellm container
kubectl exec -it $(kubectl get pod -n $NS -l app=litellm -o jsonpath='{.items[0].metadata.name}') -n $NS \
  -- env | grep OPENROUTER

echo "✅ Script completed successfully."
