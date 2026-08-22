# Containers with Docker

A container is the package of an application with all necessary dependencies
and configurations.

## Container repository

**Private**
Hosted on own servers

**Public**
Publicly hosted (e.g., Docker Hub)

## Container vs. Image

A container has layers of images.

```postgres:15.3```  Layer - application image<br>
```...```<br>
```...```<br>
```...```<br>
```alpine:3.17```  Layer - Linux base image

## Docker image (*not running*)

- The image is the actual package
- Artifact, that can moved around

## Docker container (*running*)

- The container actually starts the application
- The container environment is created

## Docker architecture and components

**Docker Engine**

- Server
- API
- CLI

**Docker Server**

- Container runtime
- Volumes
- Network
- Build images

## Docker vs. VM

- Docker virtualize the OS application layer
- Docker images are smaller
- Docker containers take seconds to start

**Problem**

Linux based container can not run on Windows or macOS kernel directly. Docker Desktop
allows to run Linux based containers on Windows or macOS (uses a hypervisor layer).

## Container port vs. Host port

Multiple container can run on the host machine. Therefore, the container port needs
to be bind to a host port (containers can have the same port).

**Example**

```docker run -p 6000:6973```

This command will bind the host port *6000* to the container port *6973*.

## Docker commands

| Command                                         | Info                                                                                                         |
|-------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| docker image                                    | Shows all images on the local machine                                                                        |
| docker ps                                       | Shows all running containers                                                                                 |
| docker ps -a                                    | Shows all running and not running containers                                                                 |
| docker run <*image*>                            | Run a new container from an image                                                                            |
| docker run -d <*image*>                         | Run the container in detached mode                                                                           |
| docker run -p <*host port*>:<*container port*>  | Bind the container port to a host port                                                                       |
| docker run --name <*container name*>            | Run the container with the specified name                                                                    |
| docker stop <*container ID/name*>               | Stop the container                                                                                           |
| docker start <*container ID/name*>              | Start a container                                                                                            |
| docker logs <*container ID/name*>               | Shows the logs of the container                                                                              |
| docker exec -it <*container ID/name*> /bin/bash | Start the terminal of the container (*-it* interactive terminal)<br>If */bin/bash* not working use */bin/sh* |

## Example - Download and run Docker container

```
docker run -e POSTGRES_PASSWORD=mysecretpassword postgres:13.10
Unable to find image 'postgres:13.10' locally
13.10: Pulling from library/postgres
b5d25b35c1db: Pull complete 
49cf892a3d6e: Pull complete 
2a0b6c31bad8: Pull complete 
30c88dd7faee: Pull complete 
8ed188c9a01e: Pull complete 
5ef46eb6901b: Pull complete 
691a93171f6d: Pull complete 
f492dbf99c64: Pull complete 
9129fcf6e316: Pull complete 
de02633c4028: Pull complete 
52882035d95f: Pull complete 
4c9d9c13a5f8: Pull complete 
ff70b8e3b3f5: Pull complete 
Digest: sha256:8f81e14286798303b82d1877bda41c6950d7866c45e721ca027886c2840d075b
Status: Downloaded newer image for postgres:13.10
...
```
If another version was already downloaded before only the layers needed for this version
will be downloaded now. This saves time and network resources.

```
docker run -e POSTGRES_PASSWORD=mysecretpassword postgres:14.7 
Unable to find image 'postgres:14.7' locally
14.7: Pulling from library/postgres
b5d25b35c1db: Already exists 
49cf892a3d6e: Already exists 
2a0b6c31bad8: Already exists 
30c88dd7faee: Already exists 
8ed188c9a01e: Already exists 
5ef46eb6901b: Already exists 
691a93171f6d: Already exists 
f492dbf99c64: Already exists 
efc373dd77fb: Pull complete 
c0dbbb6c8157: Pull complete 
b8762216f5bf: Pull complete 
fee554e21f3f: Pull complete 
dbba7b8bc5a5: Pull complete 
Digest: sha256:5ac16ee311340b09e3670d660c76f77a611202fd07b05d486e934eece99bea7c
Status: Downloaded newer image for postgres:14.7
...
```

## Example - Show running containers

```
docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS          PORTS      NAMES
9936891e686d   postgres:14.7    "docker-entrypoint.s…"   25 seconds ago   Up 24 seconds   5432/tcp   gallant_jennings
ace35922c03f   postgres:13.10   "docker-entrypoint.s…"   8 minutes ago    Up 8 minutes    5432/tcp   vigorous_blackwell
```

## Developing with Docker

See GitLab repository for an example https://gitlab.com/twn-devops-bootcamp/latest/07-docker/js-app

## Docker Compose

*docker-compose.yaml*

````yaml
version: '3'
services:
  mongodb:
    image: mongo
    ports:
     - 27017:27017
    environment:
     - MONGO_INITDB_ROOT_USERNAME=admin
     - MONGO_INITDB_ROOT_PASSWORD=password
    volumes:
     - mongo-data:/data/db
  mongo-express:
    image: mongo-express
    restart: always  # Make sure MongoExpress can connect to MongoDB container (in case MongoExpress started before MongoDB)
    ports:
     - 8081:8081
    environment:
     - ME_CONFIG_MONGODB_ADMINUSERNAME=admin
     - ME_CONFIG_MONGODB_ADMINPASSWORD=password
     - ME_CONFIG_MONGODB_SERVER=mongodb
````

| Command                                    | Info                                                                            |
|--------------------------------------------|---------------------------------------------------------------------------------|
| docker-compose -f <*yaml file name*> up    | Start the container(s). Docker compose will create a Docker Network by default. |
| docker-compose -f <*yaml file name*> down  | Stop the container(s).                                                          |

## Dockerfile

| Keyword          | Info                                       |
|------------------|--------------------------------------------|
| FROM <*image*>   | Install image                              |
| ENV <*variable*> | Set environmental variable                 |
| RUN <*command*>  | Execute Linux command                      |
| COPY             | Copy form host to container                |
| CMD              | Start the application (entrypoint command) |

**Build image**

```docker build -t <image name>:<image tag> <Dockerfile location>```

**Delete image**

| Command                    | Info             |
|----------------------------|------------------|
| docker rm <*container ID*> | Delete container |
| docker rmi <*image ID*>    | Delete image     |

Container needs to be deleted first.

## Docker registry

**Nexus config**

- Add a new repository *docker hosted*
- Add new role *nx-repository-view-docker-docker-hosted-**
- Set port (e.g., 8083) for HTTP in the repository settings
- Open port in the firewall settings
- Realms add *Docker Bearer Token*

**Configure insecure connection**

*Linux*

Add to */etc/docker/daemon.json*
```
{
    "insecure-registries":["<regestry URL:regestry port>"]
}
```

*Docker Desktop*

- Open *Preferences*
- Go to *Docker Engine*
- Insert ```"insecure-registries":["<regestry URL:regestry port>"]``` after ```"experimental..."``` line

**Login to registry**

| Command                                     | Info                                                                |
|---------------------------------------------|---------------------------------------------------------------------|
| docker login <*registry URL:registry port*> | Login token will be added to *~/.docker/config.json* on first login |

**Image naming**

```registryDomain/imageName:imageTag``` e.g., *docker.io/library/mongo:4.2*

| Command                                                                      | Info                  |
|------------------------------------------------------------------------------|-----------------------|
| docker pull <*Nexus IP:Nexus port*>/<*app name:app tag*>                     | Pull image from Nexus |
| docker tag <*app name:app tag*> <*Nexus IP:Nexus port*>/<*app name:app tag*> | Tag image             |
| docker push <*Nexus IP:Nexus port*>/<*app name:app tag*>                     | Push image to Nexus   |

**Fetch image**

```bash
curl -u <username:password> -X GET '<Nexus IP>/service/rest/v1/components?repository=<repo name>'
```

## Deploy Docker application on a server

**Add new service to the Docker Compose file**

```yaml
services:
  my-app:
    image: <docker-registry>/<app name:app tag>
    ports:
     - 3000:3000
```

## Docker volumes

Docker volumes are used for persistence data storage. The physical host file system
is mounted in the virtual file system of the container.

**Create a Docker volume**

| Command                                        | Info                                                                                          |
|------------------------------------------------|-----------------------------------------------------------------------------------------------|
| docker run -v <*host volume:container volume*> | Map the host file system to the container file system                                         |
| docker run -v <*container volume*>             | The host file system will automaticaly mapped to the container file system (anonymous volume) |
| docker run -v <*name:container volume*>        | Named volume (should be used)                                                                 |

**Add volumes to the Docker compose file**

```yaml
version: '3'
services:
  mongodb:
    #...
    volumes:
     - mongo-data:/data/db  # Location in the container
#...
volumes:
  mongo-data:
    driver: local  # Create volume on the local file system
```
All files form */data/db* inside the container will be duplicated to the *local* volume.

**Docker volume locations**

*Windows*

```C:\ProgramData\docker\volumes```

*Linux and macOS*

```/var/lib/docker/volumes```

NOTE: This path can not be accessed directly on macOS. To access the shell of the 
Docker VM in order to view volume information, use this command:
```docker run -it --privileged --pid=host debian nsenter -t 1 -m -u -n -i sh```

## Nexus as a container

https://hub.docker.com/r/sonatype/nexus3

1. Create a new droplet
2. Rename droplet
3. Edit firewall settings
4. Install Docker on the droplet
5. Create a Docker volume<br> ```docker volume create --name nexus-data```
6. Run Nexus container<br> ```docker run -d -p 8081:8081 --name nexus -v nexus-data:/nexus-data sonatype/nexus3```

By default, a user *nexus* will be created.

| Command                        | Info                                    |
|--------------------------------|-----------------------------------------|
| docker volume ls               | Shows the Docker volumes                |
| docker inspect <*volume name*> | Shows more information about the volume |

## Docker best practices

- Use official Docker images as base image.
- Use specific image version.
- User leaner OS distro (e.g., *alpine*).
- Optimize caching image layers. Order Dockerfile commands from least to most frequently changing.
- Exclude with *.dockerignore* file.
- Separate *build stage* from *runtime stage* (Multi-Stage Build).
e.g.,
```dockerfile
# Build stage
FROM maven AS build
WORKDIR /app
COPY myapp /app
RUN mvn package

# Run stage
FROM tomcat
COPY --from=build /app/target/file.war /usr/local/tomcat/...
```
- Use the least privileged user.
- Scan images for vulnerabilities with ```docker scout cves <image name:image tag>```