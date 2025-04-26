helm repo add apo https://apo-charts.oss-cn-hangzhou.aliyuncs.com
helm repo update apo


helm install apo apo/apo -n apo --create-namespace -f ./apo.yaml

# 把 ebpf 的 0 改成 9500
# kubectl edit cm -n apo apo-otel-collector-agent-config -oyaml
