

   * [v1.0.0](#v100-beta0)
      * [Deploy v1.0.0](#deploy-v1.0.0)
         * [For Quick Start](#for-quick-start)
         * [Deploy Mysql Clusters For Each Services](#deploy-mysql-clusters-for-each-services)
         * [With Moinitorig](#with-moinitorig)
         * [With Distributed Tracing](#with-distributed-tracing)
         * [Deploy All](#deploy-all)
         * [Customise Deployment](#customise-deployment)
         * [Reset Deployment](#reset-deployment)

      * [Changelog since 0.2.1](#changelog-since-v021)
         * [Features Added](#features-added)
         * [Notable Changes](#notable-changes)
         * [Test Support](#test-support)
         * [Bug fix](#bug-fix)
         
         
# v1.0.0

## Deploy v1.0.0

### For Quick Start
```bash
git clone https://github.com/FudanSELab/train-ticket.git release-1.0.0
cd train-ticket
make deploy

```

Note: if you want specify namespace, set Namespace paramter:

```bash
make deploy Namespace=yournamespace
```

### Deploy Mysql Clusters For Each Services

```bash
git clone https://github.com/FudanSELab/train-ticket.git release-1.0.0
cd train-ticket
make deploy DeployArgs="--independent-db"
```

### With Moinitorig
```bash
git clone https://github.com/FudanSELab/train-ticket.git release-1.0.0
cd train-ticket
make deploy DeployArgs="--with-monitoring"
```

### With Distributed Tracing
```bash
git clone https://github.com/FudanSELab/train-ticket.git release-1.0.0
cd train-ticket
make deploy DeployArgs="--with-tracing"
```

### Deploy All 
```bash
git clone https://github.com/FudanSELab/train-ticket.git release-1.0.0
cd train-ticket
make deploy DeployArgs="--all"
```

### Customise Deployment
You can freely combine parameters for custom deployment， for example, deploy with monitoring and tracing:

```bash
git clone https://github.com/FudanSELab/train-ticket.git release-1.0.0
cd train-ticket
make deploy DeployArgs="--with-tracing --with-monitoring"
```

### Reset Deployment

```
make reset-deploy
# if you specify namespace when deploy, set namespace as well when reset
# make reset-deploy Namespace=yournamespace
```

## Changelog since v0.2.1

### Features Added 

**Service Discovery: Nacos**

Use nacos as service register and discovery component.

Nacos use mysql cluster to store config information. 

We use nacos 2.0.1 version, for more infromation of nacos, to see: [https://nacos.io/zh-cn/docs/what-is-nacos.html
](https://nacos.io/zh-cn/docs/what-is-nacos.html)

**Gateway**

Using gateway as the only entry point for all service calls. A series of cross-cutting functions can be completed in the service gateway, such as permission verification, current limiting and monitoring, etc., which can be completed through filters.

We use spring-cloud-gateway to implement the gateway function.

**Flow Control: Sentinel**

We use Sentinel to implement the flow control for gateway.  For now, the flow control rule is simply defined in route level. We simply limited the QPS towards admin-basic-info-service to no more than 20.

To customize the flow control rule, update the configuration for Sentinel in `GatewayConfiguration.java` file.

**Monitoring: Promethues+Grafana Deployment**

We support prometheus + grafana solution in k8s deployment.

The deployment manifests of prometheus are located at：deployment/kubernetes-manifests/prometheus

**Distributed Tracing: Skywalking+ES Supoort**

We support skywalking + es solution in k8s deployment.

The deployment manifests of prometheus are located at：deployment/kubernetes-manifests/skywalking


### Notable Changes

**Log Format Unification**

Unified log format for all services

**Framework Upgrade**

Upgrade spring-boot version from 1.5.0 to 2.3.12.RELEASE.

Upgrade related dependency of services.

**Data Structrue Redesign**

Extract the common data structure of the service and put it in ts-common, instead of redefining them each service once. And data field naming is normalized.

**Dynamic Service Configuration**

Each service can dynamically configure its own database information, service discovery information, message queue information etc., (k8s deployment through configmap and secret, docker-compose deployment through environment variables) without the need to repackage the image.

**Mysql Cluster Mode Support**

Because the relational nature of the train ticket business is complex, we use a relational database, ie mysql. To support clustered deployment of mysql, we use randondb's solution for mysql deployment. For more details, see: [https://radondb.io/](https://radondb.io/)

### Test Support

We provide test scripts for functional and performance testing of train-tickets. The script provides some scenarios, such as administrator_operations, normal_query_and_booking, rebooking, rebooking_failure, search_failure, and consign_preserve.
At the same time, the script supports qos parameter setting, which can easily implement performance testing.
Access test scripts at: [https://github.com/FudanSELab/train-ticket-auto-query ](https://github.com/FudanSELab/train-ticket-auto-query)


### Bug Fix

* update order failed by the administrator.
* delete order failed by the administrator.
* delete user failed by the administrator. 
* delete price failed by the administrator.
* delete station failed by the administrator.
