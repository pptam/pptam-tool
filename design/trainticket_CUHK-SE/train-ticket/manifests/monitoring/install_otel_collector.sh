helm install clickhouse oci://registry-1.docker.io/bitnamicharts/clickhouse  --set auth.username=admin --set auth.password=password --values clickhouse_value.yaml -n monitoring

# initdbScripts:
#   create-db.sql: |
#     CREATE DATABASE IF NOT EXISTS otel; 

helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts

helm install opentelemetry-collector-daemonset open-telemetry/opentelemetry-collector --values collector_daemonset.yaml -n monitoring
helm install opentelemetry-collector-deployment open-telemetry/opentelemetry-collector --values collector_deployment.yaml -n monitoring

# kubectl patch clusterrole opentelemetry-collector --type='json' -p='[{"op": "add", "path": "/rules/-", "value": {"apiGroups":[""], "resources":["nodes/stats"], "verbs":["get", "watch", "list"]}}]'