# Container Orchestration with Kubernetes

Container orchestration tool.

**Features**
- Availability
- Scalability
- Disaster recovery

## Components

**Node** https://kubernetes.io/docs/concepts/architecture/nodes/
- Virtual or physical machine.

**Pod** https://kubernetes.io/docs/concepts/workloads/pods/
- Smallest unit in Kubernetes.
- Abstraction over containers.
- One application per *Pod*.
- Each *Pod* gets its own IP address.
- New IP address on re-creation.

**Service** https://kubernetes.io/docs/concepts/services-networking/service/
- Permanent IP address.
- Lifecycle of *Pod* and *Service* are not connected.

**Ingress** https://kubernetes.io/docs/concepts/services-networking/ingress/
- Maps traffic to different backends based on rules.

**ConfigMap** https://kubernetes.io/docs/concepts/configuration/configmap/
- External configuration of the application.

**Secret** https://kubernetes.io/docs/concepts/configuration/secret/
- Used to store secret data.

**Volume** https://kubernetes.io/docs/concepts/storage/volumes/
- Storage on local machine.
- Remote, outside the Kubernetes cluster.
- Persistence storage.

**Deployment** https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Blueprint for application *Pods*.
- Abstraction of *Pods*.

**StatefulSet** https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
- For stateful applications or databases.
- Deploying *StatefulSet* is not easy. Therefore, databases
are often hosted outside of Kubernetes clusters.

**DaemonSet** https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/
- Calculates how many replicas are needed based on existing *Nodes*.
- One replica per *Node*.
- Automatically scales up and down.

## Architecture

**Node/Worker Node**
- Has multiple *Pods*.
- Do the actual work.
- 3 processes must be installed on every *Node*.
  - *Container runtime* (e.g., containerd)
  - *Kubelet*
    - Interacts with container and Node.
    - Starts the Pods.
  - *Kube proxy*

**Control plane node**
- 4 processes run on every *control plane node*.
  - *API Server*
    - Validates requests.
  - *Scheduler*
    - Where to put a *Pod*?
  - *Controller manager*
    - Detects cluster state changes.
  - *etcd*
    - Key value store.
      - What resources are available?
      - Did the cluster state change?
      - Is the cluster healthy?

## Minikube and Kubectl

**Minikube**

https://minikube.sigs.k8s.io/docs/start/

**Kubectl**

- Command line tool.
- Talking to the *API Server*.
- Not only for *Minikube*.

*Install*

```bash
brew install minikube
```

*Start Minikube*

```bash
minikube start --driver docker
```
*Docker* is the preferred way to run *Minikube* on all operating systems.

*Minikube status*

```bash
minikube status
```
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

**Kubectl commands**

| Command                                                                | Info                                               |
|------------------------------------------------------------------------|----------------------------------------------------|
| ```kubectl get node```                                                 | Shows all available *Nodes*                        |
| ```kubectl get pods```                                                 | Shows all availabel *Pods*                         |
| ```kubectl get services```                                             | Shows all *Services*                               |
| ```kubectl create deployment <deployment name> --image=<image name>``` | Create a new deployment with the given image       |
| ```kubectl get deployments```                                          | Shows all *Deployments*                            |
| ```kubectl get replicaset```                                           | Shows the *ReplicaSets*                            |
| ```kubectl edit deployment <deployment name>```                        | Opens *Vim* for editing *Deployment* configuration |
| ```kubectl logs <pod name>```                                          | Shows the logs for the *Pod*                       |
| ```kubectl describe pod <pod name>```                                  | Shows the information of the *Pod*                 |
| ```kubectl exec --it <pod name> -- bin/bash```                         | Opens a new terminal to interact with the *Pod*    |
| ```kubectl apply -f <config-file name>.yaml```                         | Creates a *Deployment* from a config file          |
| ```kubectl delete deployment <deployment name>```                      | Deletes the *Deployment*                           |

## YAML Configuration file

The configuration file contains three parts.
1. metadata
2. specification
3. status

The *status* will be automatically be generated and added
by Kubernetes.

Example config files:
- Deployment [nginx-deployment.yaml](../media/documents/10_kubernetes/nginx-deployment.yaml)
- Service [nginx-service.yaml](../media/documents/10_kubernetes/nginx-service.yaml)

**Create *Deployment* and *Service***

*Deployment*

```bash
kubectl apply -f nginx-deployment.yaml
```

```bash
% kubectl get pod     
NAME                                READY   STATUS    RESTARTS   AGE
nginx-deployment-7577994b67-5v5n4   1/1     Running   0          3m27s
nginx-deployment-7577994b67-sb4kx   1/1     Running   0          3m27s
```

*Service*

```bash
kubectl apply -f nginx-service.yaml
```

```bash
% kubectl get services                  
NAME            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
kubernetes      ClusterIP   10.96.0.1      <none>        443/TCP   47h
nginx-service   ClusterIP   10.109.37.44   <none>        80/TCP    2m38s
```

**Delete *Deployment* and *Service***

```bash
kubectl delete -f nginx-deployment.yaml
kubectl delete -f nginx-service.yaml
```

## Demo project - Deploying Application in Kubernetes cluster

**mongo.yaml**

[mongo.yaml](../media/documents/10_kubernetes/demo_projects/deploying_app/mongo.yaml)

*Deployment* and *Service* life in the same file. *Username* and *password*
are defined in a *secrets* file and can be referenced via environmental
variables (see documentation on Docker Hub: https://hub.docker.com/_/mongo).

**mongo-secret.yaml**

[mongo-secret.yaml](../media/documents/10_kubernetes/demo_projects/deploying_app/mongo-secret.yaml)

*Username* and *password* are stored as *base64* values. To create both
values use the following commands in the terminal (replace *username* and *password*
with actual values).

```bash
echo -n 'username' | base64
echo -n 'password' | base64
```

To reference username and password this configuration needs to be
applied first.

**mongo-express.yaml**

[mongo-express.yaml](../media/documents/10_kubernetes/demo_projects/deploying_app/mongo-express.yaml)

See documentation for *mongo-express* on GitHub: https://github.com/mongo-express/mongo-express

Configuration for *mongo-express* is simular to *mongo* above.
But additional environmental variables are needed.
- DATABASE_URL     
- ME_CONFIG_MONGODB_URL

For the *service* an additional port for external connection (e.g., via browser)
needs to be configured (in range between 30000 and 32767).

**mongo-configmap.yaml**

[mongo-configmap.yaml](../media/documents/10_kubernetes/demo_projects/deploying_app/mongo-configmap.yaml)

As with the *mongo-secret.yaml* this file needs to be applied
before *mongo-express.yaml*.

**Get an IP address to connect to mongo-express**

Because this Kubernetes cluster was deployed using *Minikube*
the *mongo-express* service has no IP address.

```
% kubectl get service                        
NAME                    TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
kubernetes              ClusterIP      10.96.0.1        <none>        443/TCP          4d21h
mongo-express-service   LoadBalancer   10.101.148.199   <pending>     8081:30000/TCP   10s
mongodb-service         ClusterIP      10.107.68.220    <none>        27017/TCP        19m
```

To connect to *mongo-express* run ```minikube service <mongo-express-service name>```.
This will assign an IP address for the service and open the connection
in the browser.