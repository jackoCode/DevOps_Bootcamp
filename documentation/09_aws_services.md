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