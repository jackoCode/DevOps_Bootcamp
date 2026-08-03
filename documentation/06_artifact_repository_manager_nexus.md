# Artifact repository manager - Nexus

## Terms

| Term                |                                      |
|---------------------|--------------------------------------|
| Aritfact            | Application build into a single file |
| Artifact repository | Storage for artifacts                |

## Nexus

- Upload, store and retrieve artifacts
- Central storage
- Host own repositories (internal use) or proxy repositories (publicly available)

**Features**

- LDAP
- REST API
- Backup and restore
- Multi-format support
- Metadata (labelling and tagging)
- Cleanup policies
- Search functionality
- User token support (for system users)

### Install and run Nexus

Create a Droplet with 8GB RAM.

1. Connect to droplet via SSH ```ssh root@<droplet-ip-address>```
2. ```cd /opt```
3. Go to sonatype.com webside (https://help.sonatype.com/en/download.html) and copy the download link
![nexus_download_page.png](../media/pics/docu/06_artifact_repository_manager/nexus_download_page.png)
4. Get Nexus
![wget_nexus.png](../media/pics/docu/06_artifact_repository_manager/wget_nexus.png)
5. Unpack the downloaded archive ```tar -zxvf nexus-3.94.1-06-linux-x86_64.tar.gz```
6. ![ls_into_nexus_unpacked.png](../media/pics/docu/06_artifact_repository_manager/ls_into_nexus_unpacked.png)
7. Create a Nexus user ```adduser nexus```
8. Change ownership for both the nexus and sonatype-work folder
![chown_nexus_to_both_folder.png](../media/pics/docu/06_artifact_repository_manager/chown_nexus_to_both_folder.png)
9. Update ```vim nexus-3.94.1-06/bin/nexus.rc``` with ```run_as_user="nexus"```
10. Change user ```su - nexus```
11. Start Nexus and check port number
![nexus_started.png](../media/pics/docu/06_artifact_repository_manager/nexus_started.png)
12. Add port number to firewall rules of the droplet

**Nexus folders**

| Folder          | Info                                                                                                     |
|-----------------|----------------------------------------------------------------------------------------------------------|
| nexus-3.94.1-06 | Contains runtime and application of Nexus.                                                               |
| sonatype-work   | Contains own config and data. Update will not replace this folder. This folder is also used for backups. |


### Nexus UI

Nexus will create a new user "admin" with a default password for the first login.

### Nexus repository types

| Type       | Info                                                                                                                           |
|------------|--------------------------------------------------------------------------------------------------------------------------------|
| **proxy**  | - Linked to a remote repository (e.g., maven-central)<br/> - Act as a cache<br/> - Single endpoint for everyone                |
| **hosted** | - Primary storage<br/> - Integrated version policies<br/> - Internal releases and not external available thirdparty components |
| **group**  | - One endpoint for multiple repositories and/or groups                                                                         |

### Publish artifact

- Create Nexus user
Security -> Users
- Create Nexus role
Security -> Roles (e.g., nx-repository-view-maven2-maven-snapshots-*)

#### Gradle

#### Maven
