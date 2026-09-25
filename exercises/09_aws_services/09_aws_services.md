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


## Exercise 4


## Exercise 5


## Exercise 6


## Exercise 7


## Exercise 8


## Exercise 9

