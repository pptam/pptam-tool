







# 安装 skywalking
export SKYWALKING_RELEASE_VERSION=4.5.0
export SKYWALKING_RELEASE_NAME=skywalking  # change the release name according to your scenario
export SKYWALKING_RELEASE_NAMESPACE=monitoring    # change the namespace to where you want to install SkyWalking

helm install "$SKYWALKING_RELEASE_NAME" \
  oci://registry-1.docker.io/apache/skywalking-helm \
  --version "$SKYWALKING_RELEASE_VERSION" \
  -n "$SKYWALKING_RELEASE_NAMESPACE" \
  -f skywalking_values.yaml



helm uninstall "$SKYWALKING_RELEASE_NAME"  -n "$SKYWALKING_RELEASE_NAMESPACE"

