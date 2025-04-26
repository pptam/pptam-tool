<!--- app-name: RabbitMQ -->

# RabbitMQ packaged by helm

RabbitMQ is an open source general-purpose message broker that is designed for consistent, highly-available messaging scenarios (both synchronous and asynchronous).

[Overview of RabbitMQ](https://www.rabbitmq.com)

Trademarks: This software listing is packaged by Bitnami. The respective trademarks mentioned in the offering are owned by the respective companies, and use of them does not imply any affiliation or endorsement.
                           
## TL;DR

```bash
$ helm install my-release bitnami/rabbitmq
```

## Introduction

This chart bootstraps a [RabbitMQ](https://github.com/bitnami/containers/tree/main/bitnami/rabbitmq) deployment on a [Kubernetes](https://kubernetes.io) cluster using the [Helm](https://helm.sh) package manager.
## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+
- PV provisioner support in the underlying infrastructure

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
$ helm install my-release ./rabbitmq
```

The command deploys RabbitMQ on the Kubernetes cluster in the default configuration. The [Parameters](#parameters) section lists the parameters that can be configured during installation.

> **Tip**: List all releases using `helm list`

## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```bash
$ helm delete my-release
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Parameters

### Global parameters

| Name                      | Description                                     | Value |
| ------------------------- | ----------------------------------------------- | ----- |
| `global.imageRegistry`    | Global Docker image registry                    | `""`  |
| `global.imagePullSecrets` | Global Docker registry secret names as an array | `[]`  |
| `global.storageClass`     | Global StorageClass for Persistent Volume(s)    | `""`  |


### RabbitMQ Image parameters

| Name                | Description                                                    | Value                 |
| ------------------- | -------------------------------------------------------------- | --------------------- |
| `image.registry`    | RabbitMQ image registry                                        | `docker.io`           |
| `image.repository`  | RabbitMQ image repository                                      | `bitnami/rabbitmq`    |
| `image.tag`         | RabbitMQ image tag (immutable tags are recommended)            | `3.10.7-debian-11-r2` |
| `image.pullPolicy`  | RabbitMQ image pull policy                                     | `IfNotPresent`        |
| `image.pullSecrets` | Specify docker-registry secret names as an array               | `[]`                  |
| `image.debug`       | Set to true if you would like to see extra information on logs | `false`               |


### Common parameters

| Name                               | Description                                                                                                                                          | Value                                             |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `nameOverride`                     | String to partially override rabbitmq.fullname template (will maintain the release name)                                                             | `""`                                              |
| `fullnameOverride`                 | String to fully override rabbitmq.fullname template                                                                                                  | `""`                                              |
| `namespaceOverride`                | String to fully override common.names.namespace                                                                                                      | `""`                                              |
| `kubeVersion`                      | Force target Kubernetes version (using Helm capabilities if not set)                                                                                 | `""`                                              |
| `clusterDomain`                    | Kubernetes Cluster Domain                                                                                                                            | `cluster.local`                                   |
| `dnsPolicy`                        | DNS Policy for pod                                                                                                                                   | `""`                                              |
| `dnsConfig`                        | DNS Configuration pod                                                                                                                                | `{}`                                              |

### Statefulset parameters

| Name                                    | Description                                                                                                              | Value           |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------- |
| `replicaCount`                          | Number of RabbitMQ replicas to deploy                                                                                    | `1`             |
| `schedulerName`                         | Use an alternate scheduler, e.g. "stork".                                                                                | `""`            |
| `podManagementPolicy`                   | Pod management policy                                                                                                    | `OrderedReady`  |
| `podLabels`                             | RabbitMQ Pod labels. Evaluated as a template                                                                             | `{}`            |
| `podAnnotations`                        | RabbitMQ Pod annotations. Evaluated as a template                                                                        | `{}`            |
| `updateStrategy.type`                   | Update strategy type for RabbitMQ statefulset                                                                            | `RollingUpdate` |
| `statefulsetLabels`                     | RabbitMQ statefulset labels. Evaluated as a template                                                                     | `{}`            |
| `priorityClassName`                     | Name of the priority class to be used by RabbitMQ pods, priority class needs to be created beforehand                    | `""`            |
| `podAffinityPreset`                     | Pod affinity preset. Ignored if `affinity` is set. Allowed values: `soft` or `hard`                                      | `""`            |
| `podAntiAffinityPreset`                 | Pod anti-affinity preset. Ignored if `affinity` is set. Allowed values: `soft` or `hard`                                 | `soft`          |
| `nodeAffinityPreset.type`               | Node affinity preset type. Ignored if `affinity` is set. Allowed values: `soft` or `hard`                                | `""`            |
| `nodeAffinityPreset.key`                | Node label key to match Ignored if `affinity` is set.                                                                    | `""`            |
| `nodeAffinityPreset.values`             | Node label values to match. Ignored if `affinity` is set.                                                                | `[]`            |
| `affinity`                              | Affinity for pod assignment. Evaluated as a template                                                                     | `{}`            |
| `nodeSelector`                          | Node labels for pod assignment. Evaluated as a template                                                                  | `{}`            |
| `tolerations`                           | Tolerations for pod assignment. Evaluated as a template                                                                  | `[]`            |
| `containerSecurityContext.runAsNonRoot` | Set RabbitMQ container's Security Context runAsNonRoot                                                                   | `true`          |
| `resources.limits`                      | The resources limits for RabbitMQ containers                                                                             | `{}`            |
| `resources.requests`                    | The requested resources for RabbitMQ containers                                                                          | `{}`            |


### RBAC parameters

| Name                                          | Description                                                                                | Value  |
| --------------------------------------------- | ------------------------------------------------------------------------------------------ | ------ |
| `serviceAccount.create`                       | Enable creation of ServiceAccount for RabbitMQ pods                                        | `true` |
| `serviceAccount.name`                         | Name of the created serviceAccount                                                         | `""`   |
| `serviceAccount.automountServiceAccountToken` | Auto-mount the service account token in the pod                                            | `true` |
| `serviceAccount.annotations`                  | Annotations for service account. Evaluated as a template. Only used if `create` is `true`. | `{}`   |
| `rbac.create`                                 | Whether RBAC rules should be created                                                       | `true` |


### Persistence parameters

| Name                        | Description                                      | Value                      |
| --------------------------- | ------------------------------------------------ | -------------------------- |
| `persistence.enabled`       | Enable RabbitMQ data persistence using PVC       | `true`                     |
| `persistence.storageClass`  | PVC Storage Class for RabbitMQ data volume       | `""`                       |
| `persistence.selector`      | Selector to match an existing Persistent Volume  | `{}`                       |
| `persistence.accessModes`   | PVC Access Modes for RabbitMQ data volume        | `["ReadWriteOnce"]`        |
| `persistence.existingClaim` | Provide an existing PersistentVolumeClaims       | `""`                       |
| `persistence.mountPath`     | The path the volume will be mounted at           | `/bitnami/rabbitmq/mnesia` |
| `persistence.subPath`       | The subdirectory of the volume to mount to       | `""`                       |
| `persistence.size`          | PVC Storage Request for RabbitMQ data volume     | `8Gi`                      |
| `persistence.annotations`   | Persistence annotations. Evaluated as a template | `{}`                       |

Alternatively, a YAML file that specifies the values for the parameters can be provided while installing the chart. For example,

```bash
$ helm install my-release -f values.yaml ./rabbitmq
```

> **Tip**: You can use the default [values.yaml](values.yaml)

## Configuration and installation details

### [Rolling vs Immutable tags](https://docs.bitnami.com/containers/how-to/understand-rolling-tags-containers/)

It is strongly recommended to use immutable tags in a production environment. This ensures your deployment does not change automatically if the same tag is updated with a different image.

Bitnami will release a new chart updating its containers if a new version of the main container, significant changes, or critical vulnerabilities exist.

### Set pod affinity

This chart allows you to set your custom affinity using the `affinity` parameter. Find more information about Pod's affinity in the [kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity).

As an alternative, you can use of the preset configurations for pod affinity, pod anti-affinity, and node affinity available at the [bitnami/common](https://github.com/bitnami/charts/tree/master/bitnami/common#affinities) chart. To do so, set the `podAffinityPreset`, `podAntiAffinityPreset`, or `nodeAffinityPreset` parameters.

### Scale horizontally

To horizontally scale this chart once it has been deployed, two options are available:

- Use the `kubectl scale` command.
- Upgrade the chart modifying the `replicaCount` parameter.

> NOTE: It is mandatory to specify the password and Erlang cookie that was set the first time the chart was installed when upgrading the chart.

When scaling down the solution, unnecessary RabbitMQ nodes are automatically stopped, but they are not removed from the cluster. You need to manually remove them by running the `rabbitmqctl forget_cluster_node` command.

Refer to the chart documentation for [more information on scaling the Rabbit cluster horizontally](https://docs.bitnami.com/kubernetes/infrastructure/rabbitmq/administration/scale-deployment/).

