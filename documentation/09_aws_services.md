# AWS Services

## Introduction

**Services**

| Service                         | Info |
|---------------------------------|------|
| Compute                         | EC2  |
| Storage                         | S3   |
| Database                        |      |
| Networking                      | VPC  |
| Security, Identity & Compliance | IAM  |
| Containers                      |      |

## Scope

| Scope                  | Services and info     |
|------------------------|-----------------------|
| AWS Account            | IAM, Billing, Route53 |
| Region                 | S3, VPC, DynomoDB     |
| Availability zone (AZ) | EC2, EBS, RDS         |

## Identity and Access Management (IAM)

| IAM   | Info                                           |
|-------|------------------------------------------------|
| Users | Human or system users                          |
| Roles | AWS services and policies specific to services |

**Create *admin* user**

![new_user_specify_user_details.png](../media/pics/docu/09_aws_services/new_user_specify_user_details.png)

![new_user_set_permissions.png](../media/pics/docu/09_aws_services/new_user_set_permissions.png)
Note: Best practice is to assign permissions to *groups* and assign a group to a *user*.
In case of the user *admin* the permission can be assigned directly.

![new_user_review.png](../media/pics/docu/09_aws_services/new_user_review.png)

*Programmatic access for user admin*

This allows the user to access via the CLI.

![admin_new_access_key.png](../media/pics/docu/09_aws_services/admin_new_access_key.png)

![admin_new_access_key_tag.png](../media/pics/docu/09_aws_services/admin_new_access_key_tag.png)

## VPC

- Private network in the cloud.
- Virtual representation of network infrastructure.

**Subnet**

- Firewall rule configuration makes it either *private* or *public*.
- Example: <br> Database is running in a private subnet and the web application is running in a public subnet.
- Every subnet has an internal IP address range on the VPC level.
- Controlling access
  - Rules are created on the VPC level.
  - *Network ACLs* -> *subnet* level
  - *Security Groups* -> *instance* level

## CIDR Blocks

Range of IP addresses.

*Example*

| IPv4 CIDR     | Range                       |
|---------------|-----------------------------|
| 172.31.0.0/16 | 172.31.0.0 - 172.31.255.255 |

IP Calculator https://mxtoolbox.com/subnetcalculator.aspx <br>
IP Calculator with binary values https://jodies.de/ipcalc?host=10.0.0.0&mask1=1&mask2=

**Sub CIDR Blocks**

A CIDR block can be divided in sub CIDR blocks for multiple subnets.

*Example*

![visual_subnet_calculator.png](../media/pics/docu/09_aws_services/visual_subnet_calculator.png)

Visual subnet calculator https://www.davidc.net/sites/default/subnets/subnets.html

## EC2 Virtual Cloud Server

Repository https://gitlab.com/jackoCodes/aws-react-example#

**Launch an instance**

*Name and tags*

It is possible to assign multiple *key/value* pairs to distinguish between instances.

![ec2_name_tags.png](../media/pics/docu/09_aws_services/ec2_name_tags.png)

*Applications and OS Images*

*Amazon Linux* is a optimized Linux for AWS usage.

![ec2_app_os_image.png](../media/pics/docu/09_aws_services/ec2_app_os_image.png)

*Instance type*

![ec2_instance_type.png](../media/pics/docu/09_aws_services/ec2_instance_type.png)

*Key pair*

Create or choose a key pair to connect to the server (e.g., SSH). 

![ec2_key_pair.png](../media/pics/docu/09_aws_services/ec2_key_pair.png)

*Create key pair*

| Key file format | OS              |
|-----------------|-----------------|
| .pem            | Linux and macOS |
| .ppk            | Windows         |

![ec2_key_pair_create.png](../media/pics/docu/09_aws_services/ec2_key_pair_create.png)

After creating the key pair the private key will be downloaded automatically.
This file needs to be stored in the *.ssh* folder.

```bash
mv Downloads/<file-name>.pem ~/.ssh/
```
Also, the access right of the file needs to be changed.

```bash
chmod 400 .ssh/<file-name>.pem
```

*Network settings*

![ec2_network_settings.png](../media/pics/docu/09_aws_services/ec2_network_settings.png)

*Subnet*

The subnet in which the network interface is located. A specific subnet can be used if, for example, 
there are access rules configured.

![ec2_network_settings_subnet.png](../media/pics/docu/09_aws_services/ec2_network_settings_subnet.png)

*Source type*

| Type     | Info                                               |
|----------|----------------------------------------------------|
| Anywhere | Every IP address can access the server.            |
| Custom   | Only specified IP addresses can access the server. |
| My IP    | Only the own IP address can access the server.     |

![ec2_network_settings_source_type.png](../media/pics/docu/09_aws_services/ec2_network_settings_source_type.png)

*Configure storage*

![ec2_configure_storage.png](../media/pics/docu/09_aws_services/ec2_configure_storage.png)

**SSH into the server**

```bash
ssh -i ~/.ssh/<key-file-name>.pem ec2-user@<server-IP-address>
```
Connecting to the EC2 instance via SSH is always done with the user *ec2-user*.

**Install Docker**

Note: The package manager used on this instance is *yum*. 

If a new instance was created the first stap should always be to update the
package manager.

```bash
sudo yum update
```

*Install Docker with yum*

```bash
sudo yum install docker
```

*Start Docker*

```bash
sudo service docker start
```

*Add user ec2-user to group docker*

```bash
sudo usermod -aG docker $USER
```
Note: This change will be effective after the next login.

**Deploy Docker image**

1. Login to Docker
    ```bash
    docker login
    ```
2. Download the image
    ```bash
    docker pull <repository-name>:<tag>
    ```
3. Run
    ```bash
    docker run -d -p <server-port>:<app-port> <repository-name>:<tag> 
    ```
4. Add port <server-port> to firewall inbound rules
![ec2_edit_inbound_rules.png](../media/pics/docu/09_aws_services/ec2_edit_inbound_rules.png)

## Deploy to EC2 server from Jenkins

1. Install *SSH Agent* plugin in Jenkins.
![jenkins_plugin_ssh_agent.png](../media/pics/docu/09_aws_services/jenkins_plugin_ssh_agent.png)
2. Create a new multibranch pipeline (if not already exists).
3. Add *credentials* to the pipeline. Go to *<multibranch-pipeline> -> Credentials -> Folder -> Global*
![jenkins_add_ssh_credentials.png](../media/pics/docu/09_aws_services/aws_ecr_create_new.png)

   | Field       | Info                                                                 |
   |-------------|----------------------------------------------------------------------|
   | ID          | ID/name of the credential used in Jenkins                            |
   | Username    | The user name is always *ec2-user* for EC2 instances.                |
   | Private Key | Check *Enter directly* and copy the key file content into the field. |
4. Add the SSH agent connection to the *Jenkinsfile*.
    ```
    ...
    stage("<stage name>") {
        steps {
            script {
                sshagent(['<key ID>']) {
                    // some code
                }
    ...
    ```
   Note: In *Pipeline Syntax* the needed code can be created automatically.
![jenkins_pipeline_syntax.png](../media/pics/docu/09_aws_services/jenkins_pipeline_syntax.png)
5. Add the Jenkins IP address (for SSH) to the firewall setting on the EC2 instance.

**Note:** Docker login must be done on EC2 instance before running the pipeline.

## Docker Compose

**Install Docker Compose on EC2**

```bash
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
```
```bash
sudo chmod +x /usr/local/bin/docker-compose
```

**docker-compose.yaml**

```
version: "3.8"
services:
  java-maven-app:
    image: jackocodes/demo-repo:1.0
    ports:
      - "8080:8080"

  postgres:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_PASSWORD=my-pwd
```
**Update Jenkinsfile**

```
stage("deploy") {
    steps {
        script {
            echo "deploying docker image on EC2..."

            // Docker compose command.
            def dockerComposeCmd = "docker-compose -f docker-compose.yaml up --detach"
            sshagent(['ec2-server-key']) {

                // Copy docker-compose.yaml to EC2.
                sh "scp docker-compose.yaml ec2-user@63.187.52.210:/home/ec2-user"

                // SSH to EC2 and run Docker compose command.
                sh "ssh -o StrictHostKeyChecking=no ec2-user@63.187.52.210 ${dockerComposeCmd}"
            }
        }
    }
}
```
**Move docker-compose command to shell script**

```shell
#!/usr/bin/env bash

docker-compose -f docker-compose.yaml up --detach
echo "success"
```
*Update Jenkinsfile to use shell script*

```
stage("deploy") {
    steps {
        script {
            echo "deploying docker image on EC2..."

            // Run shell script
            def shellCmd = "bash ./server-cmd.sh"
            sshagent(['ec2-server-key']) {
                // Copy server-cmd.sh to EC2.
                sh "scp server-cmd.sh ec2-user@63.187.52.210:/home/ec2-user"

                // Copy docker-compose.yaml to EC2.
                sh "scp docker-compose.yaml ec2-user@63.187.52.210:/home/ec2-user"

                // SSH to EC2 and run Docker compose command.
                sh "ssh -o StrictHostKeyChecking=no ec2-user@63.187.52.210 ${shellCmd}"
            }
        }
    }
}
```
Note: There are more things to optimize. For example the *EC2 endpoint*
can be moved to a variable. Dynamically updating the *image version* is
also a further optimization.

## Set *image name* dynamically

**Increment version dynamically**

```
stage('increment version') {
    steps {
        script {
            echo 'incrementing app version...'
            sh 'mvn build-helper:parse-version versions:set \
                -DnewVersion=\\\${parsedVersion.majorVersion}.\\\${parsedVersion.minorVersion}.\\\${parsedVersion.nextIncrementalVersion} \
                versions:commit'
            def matcher = readFile('pom.xml') =~ '<version>(.+)</version>'
            def version = matcher[0][1]
            env.IMAGE_NAME = "$version-$BUILD_NUMBER"
        }
    }
}
```
**Commit new version to GitLab**

```
stage('commit version update'){
    steps {
        script {
            withCredentials([usernamePassword(credentialsId: 'gitlab-credentials', passwordVariable: 'PASS', usernameVariable: 'USER')]){
                sh 'git remote set-url origin https://$USER:$PASS@gitlab.com/twn-devops-bootcamp/latest/09-AWS/java-maven-app.git'
                sh 'git add .'
                sh 'git commit -m "ci: version bump"'
                sh 'git push origin HEAD:jenkins-jobs'
            }
        }
    }
}

```
## Elastic Container Registry (AWS ECR)

**Create new private repository**

![aws_ecr.png](../media/pics/docu/09_aws_services/aws_ecr.png)

![aws_ecr_create_new.png](../media/pics/docu/09_aws_services/aws_ecr_create_new.png)

*ECR push commands for the repository*

![aws_ecr_push_commands.png](../media/pics/docu/09_aws_services/aws_ecr_push_commands.png)

```bash
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 699289397297.dkr.ecr.eu-central-1.amazonaws.com
```

```bash
docker tag <app-name>:<tag> 699289397297.dkr.ecr.eu-central-1.amazonaws.com/<app-name>:<tag>
```

```bash
docker push 699289397297.dkr.ecr.eu-central-1.amazonaws.com/<app-name>:<tag>
```