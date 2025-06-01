#!/bin/bash
set -euo pipefail

### ========================================
### NETWORK EXPORT SCRIPT FOR KUBERNETES
### This script captures the entire networking layer:
### - Ingress and routing
### - Services and their endpoints
### - Network security policies
### - NodePort and exposed ports
### ========================================

# Output directory
NETWORK_DIR="k8s-network-export"
mkdir -p "$NETWORK_DIR"

echo "[1] 🔍 Exporting Ingress resources (all namespaces)"
kubectl get ingress -A -o wide > "$NETWORK_DIR/ingress-list.txt"
kubectl get ingress -A -o yaml > "$NETWORK_DIR/ingress.yaml"

echo "[2] 🔍 Exporting Services (all namespaces)"
kubectl get svc -A -o wide > "$NETWORK_DIR/services-list.txt"
kubectl get svc -A -o yaml > "$NETWORK_DIR/services.yaml"

echo "[3] 🔍 Exporting Endpoints (connects Services <-> Pods)"
kubectl get endpoints -A -o wide > "$NETWORK_DIR/endpoints.txt"
kubectl get endpoints -A -o yaml > "$NETWORK_DIR/endpoints.yaml"

echo "[4] 🔍 Exporting Network Policies"
kubectl get networkpolicy -A -o yaml > "$NETWORK_DIR/networkpolicies.yaml" || echo "⚠️ No NetworkPolicies defined"

echo "[5] 🔍 Exporting Ingress Classes"
kubectl get ingressclass -o yaml > "$NETWORK_DIR/ingressclass.yaml" || echo "⚠️ No IngressClasses defined"

echo "[6] 🔍 Listing Pod IP addresses (namespace, pod name, pod IP)"
kubectl get pods -A -o wide | awk '{print $1, $2, $7}' | column -t > "$NETWORK_DIR/pod-ip-addresses.txt"

echo "[7] 🔍 Extracting NodePort listeners (port:nodePort)"
if command -v jq &> /dev/null; then
  kubectl get svc -A -o json | jq -r '
    .items[] | select(.spec.type == "NodePort") |
    [.metadata.namespace, .metadata.name, (.spec.ports[] | "\(.port):\(.nodePort)/\(.protocol)")] |
    @tsv' > "$NETWORK_DIR/nodeport-listeners.txt"
else
  echo "⚠️ jq is not installed — skipping NodePort export"
fi

echo "✅ Networking export complete. Output in: $NETWORK_DIR/"
