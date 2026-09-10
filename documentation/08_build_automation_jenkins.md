# Build automation & CI/CD with Jenkins

## Install Jenkins

1. Create a new Droplet (minimum 1GB RAM, better 4GB)
2. Change Droplet name
3. Edit firewall settings
    - Open port 22 for SSH
    - Open port 8080 (custom) for Jenkins
   ![firewall_rules.png](../media/pics/docu/08_build_automation/firewall_rules.png)
4. SSH into Droplet ```ssh root@<droplet IP address>```
5. ```apt update```
6. ```apt install docker.io```
7. ```docker run -p 8080:8080 -p 50000:50000 -d -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts```

## Initialize Jenkins

1. ```docker exex -it <container ID> bash```
2. ```cat /var/jenkins_home/secrets/initialAdminPassword```
3. Use initial admin password for first login
![jenkins_init_page.png](../media/pics/docu/08_build_automation/jenkins_init_page.png)
4. Install suggested plugins
![jenkins_install_plugins_page.png](../media/pics/docu/08_build_automation/jenkins_install_plugins_page.png)
5. Create admin user
![jenkins_create_admin_user.png](../media/pics/docu/08_build_automation/jenkins_create_admin_user.png)

Note: The initial admin password can also be found outside the container.

The command ````docker volume inspect jenkins_home```` will return a JSON
including the "Mountingpoint" path. Within this path the *secrets* folder
can be found.

## Jenkins UI

![jenkins_ui_first_start.png](../media/pics/docu/08_build_automation/jenkins_ui_first_start.png)