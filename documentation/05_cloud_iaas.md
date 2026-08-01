# Cloud & IaaS

## IaaS
- Delegate infrastructure management
- Move infrastructure to cloud

## DigitalOcean

### Droplet
- create droplet (Ubuntu)
  - authentication via SSH
  - configure firewall
    - SSH port 22
    - set own IP address
    - assign droplet
- copy file to droplet ```scp <file> root@<droplet-ip-address>:/root``` (copy to root folder)

### Run Java app
- run java app not in attached mode ```java -jar <app.jar> &```
- check app is running ```ps aux | grep java```

### Create new user for droplet
It is best practice to create different users for running apps on the server (e.g., Jenkins user).

```
adduser jacko
usermod -aG sudo jacko  #add user to sudo group
su - jacko  #switch user
exit  #logout
```

*Add SSH key for new user*
1. Connect via SSH as root to the server ```ssh root@<server-ip-address>```
2. Copy SSH public key on local machine
3. Create *.ssh* folder in root directory of the user on the server ```mkdir .ssh```
4. Create new file *authorized_keys* ```vim .ssh/authorized_keys```
5. Past SSH public key into the *authorized_keys* file

### Nice to know things

|                       | Info                                |
|-----------------------|-------------------------------------|
| https://whatsmyip.com | Check own IP address                |
| ```netstat -lpnt```   | List servers with actual connection |
