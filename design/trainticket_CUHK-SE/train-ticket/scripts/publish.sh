#!/bin/bash
set -e

CHART_DIR="manifests/helm/trainticket"
REPO_NAME="train-ticket"
REPO_URL="https://cuhk-se-group.github.io/train-ticket"

helm dependency update $CHART_DIR

# 打包 Chart
mkdir -p .deploy
helm package $CHART_DIR -d .deploy

# 生成或更新 index.yaml
cd .deploy
if [ -f index.yaml ]; then
    helm repo index . --url $REPO_URL --merge index.yaml
else
    helm repo index . --url $REPO_URL
fi
cd ..