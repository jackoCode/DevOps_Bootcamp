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

| Command                                        | Info                                                             |
|------------------------------------------------|------------------------------------------------------------------|
| docker image                                   | Shows all images on the local machine                            |
| docker ps                                      | Shows all running containers                                     |
| docker ps -a                                   | Shows all running and not running containers                     |
| docker run <*image*>                           | Run a new container from an image                                |
| docker run -d <*image*>                        | Run the container in detached mode                               |
| docker run -p <*host port*>:<*container port*> | Bind the container port to a host port                           |
| docker run --name <*container name*>           | Run the container with the specified name                        |
| docker stop <*container ID/name*>              | Stop the container                                               |
| docker start <*container ID/name*>             | Start a container                                                |
| docker logs <*container ID/name*>              | Shows the logs of the container                                  |
| docker exec -it <*container ID/name*>          | Start the terminal of the container (*-it* interactive terminal) |

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

Example - Show running containers

```
docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS          PORTS      NAMES
9936891e686d   postgres:14.7    "docker-entrypoint.s…"   25 seconds ago   Up 24 seconds   5432/tcp   gallant_jennings
ace35922c03f   postgres:13.10   "docker-entrypoint.s…"   8 minutes ago    Up 8 minutes    5432/tcp   vigorous_blackwell
```