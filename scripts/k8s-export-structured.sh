#!/bin/bash
set -euo pipefail

### ================================
### CONFIGURATION: output directories
### ================================

# Root output directory for all exported manifests
EXPORT_DIR="k8s-structured-export"

# Define export folders per Kubernetes responsibility zone
DIR_CLUSTER_INFO="$EXPORT_DIR/cluster-info"
DIR_CORE_RESOURCES="$EXPORT_DIR/core-resources"         # Pods, Deployments, ConfigMaps, Secrets, etc.
DIR_STORAGE="$EXPORT_DIR/storage"                       # PVCs, StorageClasses
DIR_NETWORK="$EXPORT_DIR/networking"                    # Ingress, IngressClass, NetworkPolicy
DIR_RBAC="$EXPORT_DIR/access-control"                   # Roles, RoleBindings, ClusterRoles, etc.
DIR_SERVICE_ACCOUNTS="$EXPORT_DIR/service-accounts"
DIR_CRDS="$EXPORT_DIR/custom-resources"                 # CRDs + CR instances
DIR_CERTIFICATES="$EXPORT_DIR/certificates"             # cert-manager related
DIR_HELM="$EXPORT_DIR/helm-releases"                    # Helm charts rendered output

# Create all folders
mkdir -p \
  "$DIR_CLUSTER_INFO" \
  "$DIR_CORE_RESOURCES" \
  "$DIR_STORAGE" \
  "$DIR_NETWORK" \
  "$DIR_RBAC" \
  "$DIR_SERVICE_ACCOUNTS" \
  "$DIR_CRDS"/crd-objects \
  "$DIR_CERTIFICATES" \
  "$DIR_HELM"

### ================================
### 1. Cluster-level metadata
### ================================
echo "[1] Exporting cluster info"
kubectl get namespaces -o yaml > "$DIR_CLUSTER_INFO/namespaces.yaml"
kubectl get nodes -o yaml > "$DIR_CLUSTER_INFO/nodes.yaml"
kubectl version -o yaml > "$DIR_CLUSTER_INFO/version.yaml"
kubectl api-resources > "$DIR_CLUSTER_INFO/api-resources.txt"
kubectl api-versions > "$DIR_CLUSTER_INFO/api-versions.txt"
kubectl cluster-info > "$DIR_CLUSTER_INFO/cluster-info.txt"

### ================================
### 2. Core Kubernetes objects
### ================================
echo "[2] Exporting core resources: workloads, configs, pods"
for resource in deployments daemonsets statefulsets pods configmaps secrets services; do
  echo "  → $resource"
  kubectl get "$resource" --all-namespaces -o json | jq -c '.items[]' | while read -r item; do
    name=$(echo "$item" | jq -r '.metadata.name')
    ns=$(echo "$item" | jq -r '.metadata.namespace')
    echo "$item" | jq '.' > "$DIR_CORE_RESOURCES/${resource}__${ns}__${name}.json"
  done
done

### ================================
### 3. Storage configuration
### ================================
echo "[3] Exporting volumes: PVCs and StorageClasses"
kubectl get pvc --all-namespaces -o yaml > "$DIR_STORAGE/pvc.yaml"
kubectl get storageclass -o yaml > "$DIR_STORAGE/storageclasses.yaml"

### ================================
### 4. Networking and ingress
### ================================
echo "[4] Exporting network settings: ingress, ingressclass, networkpolicy"
kubectl get ingress --all-namespaces -o yaml > "$DIR_NETWORK/ingress.yaml"
kubectl get ingressclass -o yaml > "$DIR_NETWORK/ingressclass.yaml"
kubectl get networkpolicy --all-namespaces -o yaml > "$DIR_NETWORK/networkpolicies.yaml"

### ================================
### 5. Access control (RBAC)
### ================================
echo "[5] Exporting RBAC: roles, bindings, cluster-wide rules"
kubectl get roles --all-namespaces -o yaml > "$DIR_RBAC/roles.yaml"
kubectl get rolebindings --all-namespaces -o yaml > "$DIR_RBAC/rolebindings.yaml"
kubectl get clusterroles -o yaml > "$DIR_RBAC/clusterroles.yaml"
kubectl get clusterrolebindings -o yaml > "$DIR_RBAC/clusterrolebindings.yaml"

### ================================
### 6. Service Accounts
### ================================
echo "[6] Exporting service accounts"
kubectl get serviceaccounts --all-namespaces -o yaml > "$DIR_SERVICE_ACCOUNTS/serviceaccounts.yaml"

### ================================
### 7. CRDs and custom resources
### ================================
echo "[7] Exporting CRDs and all custom resource objects"
kubectl get crds -o yaml > "$DIR_CRDS/crds.yaml"

# Iterate over all registered CRDs and export their instances
kubectl get crds -o name | while read -r crd; do
  short_name=$(basename "$crd")
  echo "  → CRD object: $short_name"
  kubectl get "$short_name" --all-namespaces -o yaml > "$DIR_CRDS/crd-objects/$short_name.yaml" || true
done

### ================================
### 8. Certificates and TLS
### ================================
echo "[8] Exporting cert-manager resources"
kubectl get certificates --all-namespaces -o yaml > "$DIR_CERTIFICATES/certificates.yaml" || true
kubectl get clusterissuers --all-namespaces -o yaml > "$DIR_CERTIFICATES/clusterissuers.yaml" || true

### ================================
### 9. Helm Releases (rendered)
### ================================
echo "[9] Exporting Helm releases"
if command -v helm &> /dev/null; then
  helm list -A -q | while read -r release; do
    ns=$(helm list -A | grep "^$release" | awk '{print $2}')
    helm get all "$release" -n "$ns" > "$DIR_HELM/${ns}__${release}.txt"
  done
else
  echo "Helm not installed — skipping"
fi

echo "Export complete. All manifests saved to: $EXPORT_DIR/"
