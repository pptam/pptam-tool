#!/bin/bash

# 定义默认命名空间
NAMESPACE="monitoring"

# 函数：安装 Prometheus 堆栈
install_prometheus() {
    echo "Adding Prometheus Helm repository..."
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    echo "Updating Helm repository..."
    helm repo update
    echo "Installing Prometheus stack in namespace $NAMESPACE..."
    helm install prometheus-stack prometheus-community/kube-prometheus-stack -n $NAMESPACE
}

# 函数：卸载 Prometheus 堆栈
uninstall_prometheus() {
    echo "Uninstalling Prometheus stack from namespace $NAMESPACE..."
    helm uninstall prometheus-stack -n $NAMESPACE
    if [ "$1" = "delete-crds" ]; then
        echo "Deleting CRDs..."
        kubectl delete crd alertmanagerconfigs.monitoring.coreos.com
        kubectl delete crd alertmanagers.monitoring.coreos.com
        kubectl delete crd podmonitors.monitoring.coreos.com
        kubectl delete crd probes.monitoring.coreos.com
        kubectl delete crd prometheusagents.monitoring.coreos.com
        kubectl delete crd prometheuses.monitoring.coreos.com
        kubectl delete crd prometheusrules.monitoring.coreos.com
        kubectl delete crd scrapeconfigs.monitoring.coreos.com
        kubectl delete crd servicemonitors.monitoring.coreos.com
        kubectl delete crd thanosrulers.monitoring.coreos.com
    fi
}

# 主逻辑
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 [install|uninstall] [delete-crds]"
    exit 1
fi

ACTION=$1
DELETE_CRDS=$2

case $ACTION in
    install)
        install_prometheus
        ;;
    uninstall)
        uninstall_prometheus $DELETE_CRDS
        ;;
    *)
        echo "Invalid action: $ACTION"
        echo "Usage: $0 [install|uninstall] [delete-crds]"
        exit 1
        ;;
esac
