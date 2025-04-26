kubectl create namespace observability
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.5/cert-manager.yaml
kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.56.0/jaeger-operator.yaml -n observability