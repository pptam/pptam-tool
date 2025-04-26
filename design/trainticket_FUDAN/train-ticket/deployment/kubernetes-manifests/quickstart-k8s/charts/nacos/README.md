# Nacos Helm Chart

Nacos is committed to help you discover, configure, and manage your microservices. It provides a set of simple and useful features enabling you to realize dynamic service discovery, service configuration, service metadata and traffic management.


## Prerequisites

 - Kubernetes 1.10+ 
 - Helm v3 
 - PV provisioner support in the underlying infrastructure

## Tips
If you use a custom database, please initialize the database script yourself first.
<https://github.com/alibaba/nacos/blob/develop/distribution/conf/nacos-mysql.sql>

 
## Installing the Chart

To install the chart with `release name`:

```shell
$ helm install `release name` ./nacos
```

## Configuration

The following table lists the configurable parameters of the Skywalking chart and their default values.

| Parameter           | Description                                                        | Default                             |
|---------------------|--------------------------------------------------------------------|-------------------------------------|
| `global.mode`       | Run Mode (~~quickstart,~~ standalone, cluster; )   | `standalone`            |
| `resources`         | The [resources] to allocate for nacos container                    | `{}`                                |
| `nodeSelector`      | Nacos labels for pod assignment                   | `{}`                                |
| `affinity`          | Nacos affinity policy                                              | `{}`                                |
| `tolerations`       | Nacos tolerations                                                  | `{}`                                |
| `resources.requests.cpu`|nacos requests cpu resource|`500m`|
| `resources.requests.memory`|nacos requests memory resource|`2G`|
| `nacos.replicaCount` | Number of desired nacos pods, the number should be 1 as run standalone mode| `1`           |
| `nacos.image.repository` | Nacos container image name                                      | `nacos/nacos-server`                   |
| `nacos.image.tag`   | Nacos container image tag                                       | `2.0.1`                                |
| `nacos.image.pullPolicy` | Nacos container image pull policy                                | `IfNotPresent`                        |
| `nacos.health.enabled` | Enable health check or not                                         | `false`                              |
| `nacos.secretName`  | secret name of db for nacos                                         | `nacos-mysql`                              |
| `nacos.db.host`     | mysql  host                                                       |                                |
| `nacos.db.name`     | mysql  database name                                                      |                                |
| `nacos.db.port`     | mysql port                                                       | 3306                               |
| `nacos.db.username` | username of  database                                                       |                               |
| `nacos.db.password` | password of  database                                                       |                               |
| `nacos.env.preferhostmode` | Enable Nacos cluster node domain name support                      | `hostname`                         |
| `nacos.env.serverPort` | Nacos port                                                         | `8848`                               |
| `service.type`									| http service type													| `NodePort`			|
| `service.port`									| http service port													| `8848`				|
| `service.nodePort`								| http service nodeport												| `30000`				|
