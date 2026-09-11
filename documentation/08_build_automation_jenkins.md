# Build automation & CI/CD with Jenkins

## Install Jenkins

1. Create a new Droplet (minimum 1GB RAM, better 4GB)
2. Change Droplet name
3. Edit firewall settings
    - Open port 22 for SSH
    - Open port 8080 (custom) for Jenkins
   ![firewall_rules.png](../media/pics/docu/08_build_automation/firewall_rules.png)
4. SSH into Droplet ```ssh root@<droplet IP address>```
5. ```apt upgrade```
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

## Install build tool in Jenkins

**Maven plugin**

Install Maven plugin via Jenkins UI.
- Go to "Manage Jenkins" <br>![jenkins_manage_jenkins_icon.png](../media/pics/docu/08_build_automation/jenkins_manage_jenkins_icon.png)
- Open "Tools"
![jenkins_ui_tools.png](../media/pics/docu/08_build_automation/jenkins_ui_tools.png)
- Add Maven
![jenkins_tools_add_maven.png](../media/pics/docu/08_build_automation/jenkins_tools_add_maven.png)
- Save

**npm and Node.js**

Install npm and Node.js via terminal
- ```docker exec -u 0 -it <container ID> bash``` (0 = root user)
- Check Linux distribution ```cat /etc/issue```. This will return the Linux
distribution running in the container (e.g., ```Debian GNU/Linux 13 \n \l```)
- ```apt update```
- ```apt install curl```
- ```curl -sL https://deb.nodesource.com/setup_20.x -o nodesource_setup.sh```
- ```bash nodesource_setup.sh```
- ```apt install nodejs```

**Stage View plugin**

Install Stage View plugin via Jenkins UI.
- Go to "Manage Jenkins" <br>![jenkins_manage_jenkins_icon.png](../media/pics/docu/08_build_automation/jenkins_manage_jenkins_icon.png)
- Open "Plugins"
![jenkins_ui_plugins.png](../media/pics/docu/08_build_automation/jenkins_ui_plugins.png)
- Search for Stage View plugin
![jenkins_stage_view_plugin.png](../media/pics/docu/08_build_automation/jenkins_stage_view_plugin.png)
- Install after restart
![jenkins_stage_view_install.png](../media/pics/docu/08_build_automation/jenkins_stage_view_install.png)
- Restart Jenkins container
  - Get container ID ```docker ps -a```
  - Start container ```docker start <container ID>```

## Jenkins - Freestyle Job

**Create new Freestyle Job**

- Create a new freestyle job
![jenkins_freestyle_job_new.png](../media/pics/docu/08_build_automation/jenkins_freestyle_job_new.png)
- Add build steps
![jenkins_add_build_steps.png](../media/pics/docu/08_build_automation/jenkins_add_build_steps.png)
  - npm was installed directly in the Docker container. Therefore, it is possible
  to run npm command in a shell.
  - Maven was installed as a plugin in Jenkins. Therefore, Maven can be configured
  using a Jenkins template. This is not as flexible as running commands in a shell.

Note: More plugins (e.g., Node.js) can be installed directly in Jenkins to use it in the build steps.

**Run the job**

Run the Jenkins job with "Build Now". After the job finished the result is
shown in the "Builds" section at the bottom.

![jenkins_build_now.png](../media/pics/docu/08_build_automation/jenkins_build_now.png)

*Console Output*

![jenkins_console_output.png](../media/pics/docu/08_build_automation/jenkins_console_output.png)

**Source Code Management**

Jenkins pipelines can use code directly from a source code management tool like Gitlab.

*Configure Source Code Management for the job*

- Add repository URL
![scm_repo_url.png](../media/pics/docu/08_build_automation/scm_repo_url.png)
- Configure credentials to excess the repository
![scm_add_credentials.png](../media/pics/docu/08_build_automation/scm_add_credentials.png)
![scm_add_credentials_type.png](../media/pics/docu/08_build_automation/scm_add_credentials_type.png)
- Select branch to build
![scm_select_branch.png](../media/pics/docu/08_build_automation/scm_select_branch.png)

*Check job output*

```docker exec -it <container ID> bash```

The output of the Jenkins job can be found in ```/var/jenkins_home/workspace/```.
![jenkins_job_output.png](../media/pics/docu/08_build_automation/jenkins_job_output.png)

- *my-freestyle-job* contains the source code and the job output (e.g., jar file).
- *my-freestyle-job@tmp* is used as a temp folder while the job is running.

## Docker in Jenkins

**Setup for Docker in Jenkins**
- Stop running Jenkins container ```docker stop <container ID>```
- ```docker run -p 8080:8080 -p 50000:50000 -d -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock jenkins/jenkins:lts```
- ```docker exec -u 0 -it <container ID> bash```
- ```curl https://get.docker.com/ > dockerinstall && chmod 777 dockerinstall && ./dockerinstall```
- ```chmod 666 /var/run/docker.sock```
![docker_sock_chmod.png](../media/pics/docu/08_build_automation/docker_sock_chmod.png)

## Build Docker image

To build a Docker image from the source code a build step with the Docker command is added
(*-t* used to specify the name of the image).
![jenkins_job_build_step_docker.png](../media/pics/docu/08_build_automation/jenkins_job_build_step_docker.png)

**Console output**

```
...
[my-freestyle-job] $ /bin/sh -xe /tmp/jenkins16358888609287328001.sh
+ docker build -t java-maven-app:1.0 .
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
...
Finished: SUCCESS
```

**Docker image**

Run ```docker images``` in the terminal to get all available images.

![docker_images.png](../media/pics/docu/08_build_automation/docker_images.png)

**Push Docker image to Docker Hub**

*Create Docker Hub repository*

Create a new (private) Docker Hub repository.
![docker_hub_repo.png](../media/pics/docu/08_build_automation/docker_hub_repo.png)

*Configure Jenkins*
- Add credentials for Docker Hub login
![docker_hub_login_credentials.png](../media/pics/docu/08_build_automation/docker_hub_login_credentials.png)
- Update Jenkins job
  - Add Docker Hub credentials to the job environment
  ![jenkins_job_env_credentials.png](../media/pics/docu/08_build_automation/jenkins_job_env_credentials.png)
  - Update build step
  ![jenkins_job_build_step_docker_hub.png](../media/pics/docu/08_build_automation/jenkins_job_build_step_docker_hub.png)
  