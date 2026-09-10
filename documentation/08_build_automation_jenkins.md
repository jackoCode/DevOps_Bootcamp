# Build automation & CI/CD with Jenkins

## Install Jenkins

1. Create a new Droplet (minimum 1GB RAM, better 4GB)
2. Change Droplet name
3. Edit firewall settings
    - Open port 22 for SSH
    - Open port 8080 (custom) for Jenkins
4. SSH into Droplet
5. ```apt update```
6. ```apt install docker.io```
7. ```docker run -p 8080:8080 -p 50000:50000 -d -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts```

## Initialize Jenkins

1. ```docker exex -it <container ID> bash```
2. ```cat /var/jenkins_home/secrets/initialAdminPassword```
3. Use initial admin password for first login
4. Install suggested plugins
5. Create admin user

Note: The initial admin password can also be found outside the container.

The command ````docker volume inspect jenkins_home```` will return a JSON
including the "Mountingpoint" path. Within this path the *secrets* folder
can be found.