# Train Ticket: A New Version

## Introduction

The legacy version of Train Ticket had become outdated and lacked active maintenance. To address this, we've built a new, modernized version with improved functionality, streamlined processes, and enhanced observability.

## What's New

- **Simplified Development and Deployment**: The development workflow now fully integrates with Kubernetes (k8s) and Helm, making setup and deployment more straightforward.
- **Pruned Redundancies**: We've removed outdated or unnecessary components to improve efficiency and reduce complexity.
- **Enhanced Monitoring**: Robust monitoring is now built-in, with support for tools like [SkyWalking](https://skywalking.apache.org/), [OpenTelemetry](https://opentelemetry.io/), [APO](https://kindlingx.com/docs/APO%20%E5%90%91%E5%AF%BC%E5%BC%8F%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7%E4%B8%AD%E5%BF%83/%E5%AE%89%E8%A3%85%E6%89%8B%E5%86%8C/%E5%BF%AB%E9%80%9F%E9%83%A8%E7%BD%B2/%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B), providing deep insights into system performance.

## Prerequisites

Before you begin, ensure you have the following tools installed:

1. **[Helm](https://helm.sh/docs/intro/install/)**: For managing Kubernetes applications.
2. **[Skaffold](https://skaffold.dev/docs/install/)**: For building Docker images.
3. **[Minikube](https://minikube.sigs.k8s.io/docs/start/)**: For running a local Kubernetes cluster (optional for local development).
4. **Docker**: For building container images.
5. **JDK and Maven**: For building the Java-based project. (JDK 8 or 17 is recommended; ensure your `JAVA_HOME` is set correctly.)
   - You can check your Java version with:
     ```bash
     java -version
     ```
   - Maven can be installed via package managers or downloaded from the [Apache Maven website](https://maven.apache.org/download.cgi).

You’ll also need access to a container registry (e.g., Docker Hub, a private registry) to push and pull images.


## Development Guide

Follow these steps to build the project:

1. **Build the Project**:
   ```bash
   mvn clean package -Dmaven.test.skip=true
   ```

2. **Build Docker Images with Skaffold**:
   ```bash
   skaffold build --default-repo=<your-registry>
   ```
   - Replace `<your-registry>` with a registry you have push access to (e.g., `docker.io/yourusername`, `gcr.io/yourproject`).
   - Example: `skaffold build --default-repo=docker.io/myuser`.
   - This builds and pushes images to the specified registry.


## Deployment Instructions

Before deploying the application, you must build the Helm dependencies:

1. **Build Helm Dependencies**:
   ```bash
   helm dependency build manifests/helm/generic_service
   ```
   This step is mandatory and will fetch all required dependencies specified in Chart.yaml (mysql, postgresql, rabbitmq, etc.).

2. **Basic Deployment with Specific Image Tag**:


```bash
# alter: use the published helm chart
helm repo add train-ticket https://cuhk-se-group.github.io/train-ticket
helm repo update
helm search repo train-ticket
```


```bash
helm install ts manifests/helm/generic_service -n ts --create-namespace \
   --set global.monitoring=opentelemetry \
   --set skywalking.enabled=false \
   --set global.image.tag=3384da1c
```
- `ts`: Release name (customizable).
- `-n ts`: Namespace (created if it doesn’t exist).
- `--set`: Customizes deployment options (e.g., monitoring type, image tag).



3. **Using Custom Image Registry**:
   ```bash
   helm install ts manifests/helm/generic_service -n ts --create-namespace \
     --set global.monitoring=opentelemetry \
     --set skywalking.enabled=false \
     --set global.image.tag=latest \
     --set global.image.repository=registry.cn-shenzhen.aliyuncs.com/lincyaw
   ```

4. **Advanced Example (with APO)**:
   To enable specific configurations (e.g., nodePort for UI):
   ```bash
   helm upgrade ts manifests/helm/generic_service -n ts-dev --create-namespace \
     --set global.monitoring=opentelemetry \
     --set opentelemetry.enabled=false \
     --set services.tsUiDashboard.nodePort=30081 \
     --set global.image.tag=310a67e0
   ```

5. **Uninstall**:
   To remove the deployment:
   ```bash
   helm uninstall ts -n ts
   ```

Note: If you change the release name, you must also update the values.yaml file accordingly. For instance, when disabling the PostgreSQL component for demo purposes (not recommended for production), ensure you configure the host to match your PostgreSQL service's hostname, as shown below:

```yaml
postgresql:
  enabled: false # To disable the demo PostgreSQL deployment (not for production use).
  config:
    # Specify your PostgreSQL service's hostname (effective when postgresql.enabled is false).
    host: ts-postgresql # Important: Update this to match your service name!
  auth:
```

This new version is designed to offer a more streamlined, efficient, and powerful solution for managing train ticket services, leveraging the latest in technology and best practices.