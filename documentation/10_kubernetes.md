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

## Namespaces

*Namespace* is a virtual cluster inside a cluster.

**Default Namespaces**

```kubectl get namespace```

| Namespace       | Info                                                                               |
|-----------------|------------------------------------------------------------------------------------|
| kube-system     | System processes. Do **not** create or modify.                                     |
| kube-public     | Publicly accessable data. It is a *ConfigMap*, which contains cluster information. |
| kube-node-lease | Heardbeats of *Nodes*. Each Node has associated lease object.                      |
| default         | Resources, which are created are located here.                                     |

**Create a Namespace**

1. Command line ```kubectl create namespace <namespace name>```
2. Config file
   e.g., 
   ```yaml
   apiVersion: v1
   kind: Namespace
   metadata:
      name: <namespace name>
   ```
   
**Usage**

- Group resources in a Namespace (e.g., Database, Monitoring, Elastic Stack, Nginx-Ingress).
- Many teams, same application.
- Resource sharing
  - Staging and deployment
  - Blue/green deployment
- Access and resource limits on Namespaces

**Characteristics**

- Can not access most resources from another Namespace (*ConfigMag* for each Namespace is needed).
- Access *Service* in another Namespace.
- Components that can not be created within a Namespace.
  - Live globally in a cluster.
  - Can not isolate them.

**Create a component in a Namespace**

- Command line ```kubectl apply -f <configmap>.yaml --namespace=<namespace name>```
- Config file
  e.g.,
  ```yaml
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: mongodb-configmap
    namespace: my-namespace
  data:
    database_url: mongodb-service.database
  ```

*Get Namespace information*

Not bound to a Namespace.
```bash
kubectl api-resources --namespaced=false
```

Bound to a Namespace.
```bash
kubectl api-resources --namespaced=true
```

**Change the active Namespace**

- Command line
  ```bash
  kubectl config set-current --current --namespace=<namespace name>
  ```
- Using *kubectx* (https://github.com/ahmetb/kubectx).

## Service

- Stable IP address for Pods.
- Load balancing.
- Loose coupling.

### ClusterIP Service

- Default type.
- ```kubectl get pod -o wide``` gives additional information of the Pods including the IP addresses.
- Abstraction layer for IP addresses (e.g., Ingress calls the Service and the Service handles the request).

*Which Pods to forward?*

- "selector" attribute
  - Pods are identified via selectors
  - Key value pair
  - Labels of Pods
  - Random label names

*Pod* has an attribute "labels"
```yaml
labels:
  app: my-app
  type: microservice
```

*Service* matches this label
```yaml
selector:
  app: my-app
  type: microservice
```

*Which port to forward request to?*

- "targetPort" attribute
  - Application port is listening at this port

### Multi-Port Service

- Handles requests to multiple ports.

### Headless Service

- Client wants to communicate with one specific Pod directly.
- Pods want to talk directly with a specific Pod.
- Not randomly selected.
- *ClusterIP* and *Headless* Service are running in parallel.

**Use case**: Stateful applications like databases.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb-service-headless
spec:
  clusterIP: None # for headless service clusterIP must be None
  selector:
    app: mongodb
  ports:
    - protocol: TCP
      port: 27017
      targetPort: 27017
```

### NodePort Service

- External traffic has access to fixed port on each *worker Node*.
- Port must be in range between 30000 and 32767.

**Node:** NodePort services are **not** secure! Not for external connection, only for testing.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ms-service-nodeport
spec:
  type: NodePort
  selector:
    app: microservice-one
  ports:
    - protocol: TCP
      port: 3200
      targetPort: 3000
      nodePort: 30008
```

### LoadBalancer Service

- Access externally through cloud providers load balancer.
- *NodePort* and *ClusterIP* service are created automatically.

*LoadBalancer* is an extension of *NodePort* is an extension of *ClusterIP*.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ms-service-loadbalancer
spec:
  type: LoadBalancer
  selector:
    app: microservice-one
  ports:
    - protocol: TCP
      port: 3200
      targetPort: 3000
      nodePort: 30010
```

## Ingress

**Example**

*Ingress*
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp-internal-service
                port:
                  number: 8080
```

*Internal service*
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-internal-service
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
```

### Ingress Controller

https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/

- Evaluates all the rules.
- Manages redirections.
- Entrypoint to cluster.
- Many third-party implementations (e.g., nginx https://docs.nginx.com/nginx-ingress-controller/install/helm/open-source).

**Install *Ingress Controller* in Minikube**

```helm install nginx-ingress oci://ghcr.io/nginx/charts/nginx-ingress```

Run nginx dashboard: ```minikube dashboard```

**Create Ingress rule**

[dashboard-ingress.yaml](../media/documents/10_kubernetes/demo_projects/ingress/dashboard-ingress.yaml)

```kubectl apply -f dashboard-ingress.yaml```

Get information 

```kubectl get ingress -n kubernetes-dashboard```
```
NAME                CLASS   HOSTS           ADDRESS   PORTS   AGE
dashboard-ingress   nginx   dashboard.com             80      43s
```

To connect to *dashboard.com* on the local machine, the */etc/hosts* file needs to be updated.

1. ```sudo vim /etc/hosts```
2. Insert *127.0.0.1 &emsp; dashboard.com*
3. Run dashboard with ```minikube tunnel```
4. Access dashboard in browser with *dashboard.com*

### More use cases

**Multiple paths for same host.**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: simple-fanout-example
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.com
      http:
        paths:
          - path: /analytics
            backend:
              service:
                name: analytics-service
                port:
                  number: 3000
          - path: /shopping
            backend:
              service:
                name: shopping-service
                port:
                  number: 8080
```

**Multiple sub-domains or domains.**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: name-virtual-host-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: analytics.myapp.com
      http:
        paths:
          - path: /
            backend:
              service:
                name: analytics-service
                port:
                  number: 3000
    - host: shopping.myapp.com
      http:
        paths:
          - path: /
            backend:
              service:
                name: shopping-service
                port:
                  number: 8080
```

### Configure *TLS* certificate (https://)

*Ingress*

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-example-ingress
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - myapp.com
    secretName: myapp-secret-tls
  rules:
    - host: myapp.com
      http:
        paths:
          - path: /analytics
            backend:
              service:
                name: myapp-internal-service
                port:
                  number: 8080
```

*Secret*

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret-tls
  namespace: default
data:
  tls.crt: <base64 encoded cert>
  tls.key: <base64 encoded key>
type: kubernetes.io/tls
```

1. Data key need to be *tls.crt* and *tls.key*.
2. Values are file contents **NOT** file paths/locations.
3. Secret component must be in the *same namespace* as the Ingress component.

## Gateway API

https://kubernetes.io/docs/concepts/services-networking/gateway/

**Benefits**
1. Configuration decoupled.
2. Native traffic control.
3. One entry point for all traffic types.

*Note*: Ingress is still valid for
- few services,
- single teams and
- standard HTTP.

## Persisting data with *Volumes*

### Persistent Volume

- Cluster resource.
- Created via YAML file.
  - kind: PersistentVolume
  - spec: e.g., how much storage?
- Needs actual physical storage.
  - You need to *create* and *manage* them by yourself.
- **NOT** namespaced.

### Persistent Volume Claim

- Pod requests the volume through the *PVC*.
- Claim tries to find a volume in the cluster.
- Volume has the actual storage backend.
- *Claim* must be in the same namespace as the Pod (because
  Persistent Volume is not namespaced).

### Storage Class

- Provisions Persistent Volumes *dynamically* when Persistent Volume Claim claims it.
- Created via YAML file.
  - kind: StorageClass
  - Attribute *provisioner*.
    - Each storage backend has own *provisioner*.
    - Internal provisioner starts with *kubernetes.io*.
    - External provisioner available.
  - Configure parameters for storage we want to request for PV (e.g., *fsType: ext4*).

**Process**

1. *Pod* claims storage via *Persistent Volume Claim*.
2. *Persistent Volume Claim* requests storage from *Storage Class*.
3. *Storage Class* creates *Persistent Volume* that meets the needs of the claim.

## ConfigMap & Secret

Demo files: [configset_secret](../media/documents/10_kubernetes/demo_projects/configset_secret)

*ConfigMap* and *Secret* must be created and exist before Pod
starts in the Kubernetes cluster.

```
kubectl apply -f config-file.yaml
kubectl apply -f secret-file.yaml
```

```
kubectl get configmap

NAME                            DATA   AGE
mosquitto-config-file           1      53s
```

```
kubectl get secret

NAME                                  TYPE                 DATA   AGE
mosquitto-secret-file                 Opaque               1      13s
```

```
kubectl apply -f mosquitto.yaml
```

```
kubectl exec -it mosquitto-765cbd6d8f-m9d74 -- /bin/sh 

# cd mosquitto/
/mosquitto # cd config
/mosquitto/config # ls
mosquitto.conf

/mosquitto/config # cd ..
/mosquitto # ls
config  data    log     secret
```

## StatefulSet

Used for stateful application (e.g., databases).

- State**less** applications are deployed using *Deployment*
- State**ful** applications are deployed using *StatefulSet*

**Pod identity**

- Unique ID.
- Replica will be created only main is already running.

**Replicating stateful applications**

- It is complex.
- Kubernetes helps.
- Still need to do
  - configure cloning and data synchronization,
  - make remote storage available, and
  - manage and backup.
- Stateful applications **not** perfect for containerized environments.

## Managed Kubernetes Services

- Only care about *worker nodes*.
- Everything pre-installed.
- *Control plane nodes* created and managed by cloud provider.
- Only pay for worker nodes.
- Less effort and time.

## Helm

Package manager for Kubernetes.

**Helm Charts**

- Bundle of YAML files.
- Create own *Helm Charts* with *Helm*.
- Push to Helm repository.
- Download and use existing ones.

**Templating Engine**

- Define a common blueprint.
- Dynamic values are replaced by placeholders. {{ .Values. ... }} -> values.yaml file.

**Structure**

```
mychart             Top level folder -> name of chart.
|-- Chart.yaml      Meta info about chart.
|-- values.yaml     Values for the template files.
+-- chats           Chart dependencies.
+-- templates       Actual template files.
```

**Release Management**

### Helm Demo

- The installation documentation for helm can be found here: https://helm.sh/docs/intro/install/
- The Bitnami helm chart repository information commands can be found here: https://github.com/bitnami/charts/tree/main/bitnami/mongodb

*Values file*

[helm-mongodb.yaml](../media/documents/10_kubernetes/helm_demo/helm-mongodb.yaml)

*Deployment*

[helm-mongo-express.yaml](../media/documents/10_kubernetes/helm_demo/helm-mongo-express.yaml)

*Ingress*

[helm-ingress.yaml](../media/documents/10_kubernetes/helm_demo/helm-ingress.yaml)

## Deploying Images in Kubernetes from private Docker repository

**Steps to pull image form private registry**

1. Create *Secret* component with credentials for Docker registry.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-registry-key
data:
  .dockerconfigjson:<base64 encoded token>
type: kubernetes.io/dockerconfigjson
```

2. Configure *Deployment/Pod*. Use *Secret* using **imagePullSecrets**.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <app name>
  labels:
    app: <app name>
spec:
  replicas:
  selector:
    matchLabels:
      app: <app name>
  template:
    metadata:
      labels:
        app: <app name>
    spec:
      imagePullSecret:
        - name: <registry-key name>
      containers:
        - name: <app name>
          image: <image name>
          imagePullPolicy: Always
          ports:
            - containerPort: 3000
```

*Create docker login secret from config.json file*
```
kubectl create secret generic <registry-key name> --from-file=.dockerconfigjson=.docker/config.json --type=kubernetes.io/dockerconfigjson
```
This can be used if multiple registries are in use, because
config.json file can contain registry keys for more then one
private Docker registry.

*Create Docker login secret with login credentials*
```
kubectl create secret docker-registry <registry-key name> --docker-server=<server URL> --docker-username=<username> --docker-password=<password>
```
This can only be used for one registry.

**Useful CLI commands**

| Command                                                                                           | Info                                               |
|---------------------------------------------------------------------------------------------------|----------------------------------------------------|
| ```aws ecr get-login-password```                                                                  | Print full Docker login command for AWS ECR.       |
| ```docker login -u <username> -p <password>```                                                    | Login to Docker private repository.                |
| ```cat .docker/config.json \| base64```                                                           | Base64 encode config file.                         |
| ```kubectl get secret```                                                                          | Access generated secret.                           |
| ```minikube ssh```                                                                                | Access minikube console.                           |
| ```minikube cp minikube:/home/docker/.docker/config.json /users/<username>/.docker/config.json``` | Copy config.json file from Minikube to local host. |

## Operator

*Stateless*

No control necessary after the application is deployed.

*Stateful*

- Data persistence.
- Manual intervention necessary.

**Operator** replaces human operator with software operator.
- Control loop mechanism.
- Makes use of CRDs (Custom Resource Definition).
- Domain/app-specific knowledge.

There are *Operators* available for common used applications (e.g., https://operatorhub.io). 
Own *Operators* can be created with the **Operator SDK** (https://sdk.operatorframework.io).

## Authorization with *Role Based Access Control* (RBAC)

### Users
**Role**

- Defines namespace permissions.
- Bound to a specific namespace.
- What resources in that namespace can be accessed.
- What actions can be performed with these resources.
- Defines resources and access permissions, but no information on who gets these permissions.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: my-app
  name: developer
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "create", "list"]
  - apiGroups: [""]
    resources: ["secret"]
    verbs: ["get"]
```

|           | Info                                                |
|-----------|-----------------------------------------------------|
| namespace | Optional. Define a Role for a specific application. |
| apiGroups | "" indicates the core API group.                    |
| resources | K8s components like Pods, Developments etc.         |
| verbs     | The action on a resource.                           |


**RoleBinding**

- Link ("bind") a Role to a user or group.
- All members of the group get permissions defined in the Role.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: jane-developer-binding
subjects:
  - kind: User
    name: jane
    apiGroups: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroups: rbac.authorization.k8s.io
```

### Admins
**ClusterRole**

- Defines resources and permissions cluster wide.
- Attach *ClusterRole* using *ClusterRoleBinding*.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-admin
rules:
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get", "create", "list", "delete", "update"]
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: read-secret-global
subjects:
  - kind: Group
    name: cluster-admins
    apiGroups: rbac.authorization.k8s.io
roleRef:
  - kind: ClusterRole
    name: cluster-admin
    apiGroups: rbac.authorization.k8s.io
```

### External sources for authentication

Kubernetes does not manage users natively.

User authentication:
- Static token file
- Certificates
- 3rd party identity service

### Service accounts

- Applications are inside or outside the cluster.
- Link *ServiceAccount* to *Role* with *RoleBinding*.
- Link *ServiceAccount* to *ClusterRole* with *ClusterRoleBinding*.

## Microservices in Kubernetes

**Information needed form developers**
- What microservice to deploy?
- Which microservice is talking to which microservice?
- How are they communicating?
  - API call.
  - Message broker.
  - Service mesh.
- Which database are they using?
- 3rd party services.
- On which port does each microservice run?

**Prepare Kubernetes environment**
- Deploy any 3rd party applications.
- Create *Secrets* and *ConfigMaps* for microservices.
- Create *Deployment* and *Service* for each microservice.

