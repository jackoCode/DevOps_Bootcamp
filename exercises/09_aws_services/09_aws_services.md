# AWS Services

## Exercise 1

**Create user group *devops***

```bash
aws create-group --group-name devops
```

```
{
    "Group": {
        "Path": "/",
        "GroupName": "devops",
        "GroupId": "AGPA2FUHFNAY36UYTGQDY",
        "Arn": "arn:aws:iam::699289397297:group/devops",
        "CreateDate": "2026-09-25T12:31:08+00:00"
    }
}
```
**Create user *jacko***

```bash
aws create-user --user-name jacko
```

```
{
    "User": {
        "Path": "/",
        "UserName": "jacko",
        "UserId": "AIDA2FUHFNAYVHPRK24EZ",
        "Arn": "arn:aws:iam::699289397297:user/jacko",
        "CreateDate": "2026-09-25T12:32:32+00:00"
    }
}
```
**Add user to group**

```bash
aws iam add-user-to-group --user-name jacko --group-name devops
aws iam get-group --group-name devops
```

```
{
    "Users": [
        {
            "Path": "/",
            "UserName": "jacko",
            "UserId": "AIDA2FUHFNAYVHPRK24EZ",
            "Arn": "arn:aws:iam::699289397297:user/jacko",
            "CreateDate": "2026-09-25T12:32:32+00:00"
        }
    ],
    "Group": {
        "Path": "/",
        "GroupName": "devops",
        "GroupId": "AGPA2FUHFNAY36UYTGQDY",
        "Arn": "arn:aws:iam::699289397297:group/devops",
        "CreateDate": "2026-09-25T12:31:08+00:00"
    }
}
```
**Attach permissions to group**

*EC2 full access*

```bash
aws iam attach-group-policy --group-name devops --policy-arn "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
```
*VPC full access*

```bash
aws iam attach-group-policy --group-name devops --policy-arn "arn:aws:iam::aws:policy/AmazonVPCFullAccess"
```
**Create login profile for first login**

```bash
aws iam create-login-profile --user-name jacko --password MyPassword! --password-reset-required
```

```
{
    "LoginProfile": {
        "UserName": "jacko",
        "CreateDate": "2026-09-25T12:44:11+00:00",
        "PasswordResetRequired": true
    }
}
```
**Add changePwd policy to group**

```bash
aws iam attach-group-policy --group-name devops --policy-arn arn:aws:iam::699289397297:policy/changePwd
aws iam list-attached-group-policies --group-name devops
```
```
{
    "AttachedPolicies": [
        {
            "PolicyName": "changePwd",
            "PolicyArn": "arn:aws:iam::699289397297:policy/changePwd"
        },
        {
            "PolicyName": "AmazonEC2FullAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
        },
        {
            "PolicyName": "AmazonVPCFullAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AmazonVPCFullAccess"
        }
    ]
}
```
Sign in with user *jacko* and change password.

**Create access key for user**

```bash
aws iam create-access-key --user-name jacko
```

```
{
    "AccessKey": {
        "UserName": "jacko",
        "AccessKeyId": "...",
        "Status": "Active",
        "SecretAccessKey": "...",
        "CreateDate": "2026-09-25T12:54:07+00:00"
    }
}
```

## Exercise 2

**Configure AWS CLI for user *jacko***

```bash
aws configure
AWS Access Key ID [****************]: ...
AWS Secret Access Key [****************]: ...
Default region name [eu-central-1]: eu-central-1
Default output format [json]: json
```

## Exercise 3

*Create VPC*

```bash
aws ec2 create-vpc --cidr-block 10.0.0.0/24 --query Vpc.VpcId --output text
```
```
vpc-034843c06897148b1
```

*Create subnet*

```bash
aws ec2 create-subnet --vpc-id vpc-034843c06897148b1 --cidr-block 10.0.0.0/24 --availability-zone eu-central-1a --query Subnet.SubnetId --output text
```
```
subnet-04caf188718e0d77a
```

*Create internet gateway*

```bash
aws ec2 create-internet-gateway --query InternetGateway.InternetGatewayId --output text
```
```
igw-059b50991677d84a4
```

*Attach internet gateway to VPC*

```bash
aws ec2 attach-internet-gateway --vpc-id vpc-034843c06897148b1 --internet-gateway-id igw-059b50991677d84a4
```

*Create route table for public subnet*

```bash
aws ec2 create-route-table --vpc-id vpc-034843c06897148b1 --query RouteTable.RouteTableId --output text
```
```
rtb-0e7758b593584bf3e
```

*Add a route to send traffic to the internet gateway*

```bash
aws ec2 create-route --route-table-id rtb-0e7758b593584bf3e --destination-cidr-block 0.0.0.0/0 --gateway-id igw-059b50991677d84a4
```
```
{
    "Return": true
}
```

*Associate route table with public subnet*

```bash
aws ec2 associate-route-table --route-table-id rtb-0e7758b593584bf3e --subnet-id subnet-04caf188718e0d77a
```
```
{
    "AssociationId": "rtbassoc-0d7356f40fe6e747a",
    "AssociationState": {
        "State": "associated"
    }
}
```

*Create security group*

```bash
aws ec2 create-security-group --group-name my-sg-exercise --description "My security group for exercise 09" --vpc-id vpc-034843c06897148b1
```
```
{
    "GroupId": "sg-0cfc4c761e7fe38c7",
    "SecurityGroupArn": "arn:aws:ec2:eu-central-1:699289397297:security-group/sg-0cfc4c761e7fe38c7"
}
```

*Find own public IP address*

```bash
curl https://checkip.amazonaws.com
```
```
80.144.169.16
```

*Add SSH inbound rule for port 22*

```bash
aws ec2 authorize-security-group-ingress --group-id sg-0cfc4c761e7fe38c7 --protocol tcp --port 22 --cidr 0.0.0.0/0
```
```
{
    "Return": true,
    "SecurityGroupRules": [
        {
            "SecurityGroupRuleId": "sgr-080fa69c83fb66a3a",
            "GroupId": "sg-0cfc4c761e7fe38c7",
            "GroupOwnerId": "699289397297",
            "IsEgress": false,
            "IpProtocol": "tcp",
            "FromPort": 22,
            "ToPort": 22,
            "CidrIpv4": "0.0.0.0/0",
            "SecurityGroupRuleArn": "arn:aws:ec2:eu-central-1:699289397297:security-group-rule/sgr-080fa69c83fb66a3a"
        }
    ]
}
```

*Add inbound rule for port 3000 (Node.js)*

```bash
aws ec2 authorize-security-group-ingress --group-id sg-0cfc4c761e7fe38c7 --protocol tcp --port 3000 --cidr 0.0.0.0/0
```
```
{
    "Return": true,
    "SecurityGroupRules": [
        {
            "SecurityGroupRuleId": "sgr-024dabb1f4fc3a294",
            "GroupId": "sg-0cfc4c761e7fe38c7",
            "GroupOwnerId": "699289397297",
            "IsEgress": false,
            "IpProtocol": "tcp",
            "FromPort": 3000,
            "ToPort": 3000,
            "CidrIpv4": "0.0.0.0/0",
            "SecurityGroupRuleArn": "arn:aws:ec2:eu-central-1:699289397297:security-group-rule/sgr-024dabb1f4fc3a294"
        }
    ]
}
```

*Check security group rules*

```bash
aws ec2 describe-security-groups --group-ids sg-0cfc4c761e7fe38c7
```
```
{
    "SecurityGroups": [
        {
            "GroupId": "sg-0cfc4c761e7fe38c7",
            "IpPermissionsEgress": [
                {
                    "IpProtocol": "-1",
                    "UserIdGroupPairs": [],
                    "IpRanges": [
                        {
                            "CidrIp": "0.0.0.0/0"
                        }
                    ],
                    "Ipv6Ranges": [],
                    "PrefixListIds": []
                }
            ],
            "VpcId": "vpc-034843c06897148b1",
            "SecurityGroupArn": "arn:aws:ec2:eu-central-1:699289397297:security-group/sg-0cfc4c761e7fe38c7",
            "OwnerId": "699289397297",
            "GroupName": "my-sg-exercise",
            "Description": "My security group for exercise 09",
            "IpPermissions": [
                {
                    "IpProtocol": "tcp",
                    "FromPort": 22,
                    "ToPort": 22,
                    "UserIdGroupPairs": [],
                    "IpRanges": [
                        {
                            "CidrIp": "0.0.0.0/0"
                        }
                    ],
                    "Ipv6Ranges": [],
                    "PrefixListIds": []
                },
                {
                    "IpProtocol": "tcp",
                    "FromPort": 3000,
                    "ToPort": 3000,
                    "UserIdGroupPairs": [],
                    "IpRanges": [
                        {
                            "CidrIp": "0.0.0.0/0"
                        }
                    ],
                    "Ipv6Ranges": [],
                    "PrefixListIds": []
                }
            ]
        }
    ]
}

```

## Exercise 4

*Create EC2 instance*

```bash
aws ec2 run-instances 
  --image-id ami-06121aa3085b6f918 
  --count 1 
  --instance-type t3.micro 
  --key-name MyKpCli 
  --security-group-ids sg-0cfc4c761e7fe38c7 
  --subnet-id subnet-04caf188718e0d77a
  --associate-public-ip-address
```
```
"InstanceId": "i-01da92185c0fec243"
```

```bash
aws ec2 describe-instances --instance-id i-01da92185c0fec243 --query "Reservations[*].Instances[*].{State:State.Name,Address:PublicIpAddress}"
```
```
[
    [
        {
            "State": "running",
            "Address": "3.76.100.192"
        }
    ]
]
```

## Exercise 5

*SSH into server*

```bash
ssh -i ~/.ssh/<key-file-name>.pem ec2-user@3.76.100.192
```

*Install Docker*

```bash
sudo yum update
sudo yum install docker
sudo service docker start
sudo usermod -aG docker $USER
```

## Exercise 6, 7, 9

Repository: https://gitlab.com/jackoCodes/aws-exercise/

## Exercise 8

*Open port 3000*

```bash
aws ec2 authorize-security-group-ingress 
  --group-id sg-0cfc4c761e7fe38c7 
  --protocol tcp 
  --port 3000 
  --cidr 0.0.0.0/0
```
