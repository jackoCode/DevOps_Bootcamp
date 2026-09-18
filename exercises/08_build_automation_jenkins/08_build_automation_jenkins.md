# Exercise - Build Automation & CI/CD with Jenkins

GitLab repository: https://gitlab.com/jackoCodes/jenkins-exercise#

## Exercise 1

```dockerfile
FROM node:24-alpine

RUN mkdir -p /my-app
COPY app/ /my-app/

WORKDIR /my-app
EXPOSE 3000

RUN npm install
CMD ["node", "server.js"]
```

## Exercise 2

```
pipeline {
    agent any
    tools {
        nodejs 'nodejs'
    }
    stages {
        stage("Increment version") {
            steps {
                script {
                    dir("app") {
                        // More information about npm version https://docs.npmjs.com/cli/v7/commands/npm-version
                        sh "npm version minor -no-git-tag-version"  // version "patch", "minor" or "major" possible
                        def packageJson = readJSON file: 'package.json'
                        def version = packageJson.version
                        env.IMAGE_VERSION = "$version-$BUILD_NUMBER"  // BUILD_NUMBER is standard Jenkins env
                    }
                }
            }
        }
        stage("Testing") {
            steps {
                script {
                    dir("app") {
                        sh "npm install"
                        sh "npm run test"
                    }
                }
            }
        }
        stage("Build and publish image") {
            steps {
                withCredentials([usernamePassword(credentialsId: "docker", usernameVariable: "USER", passwordVariable: "PASS")]) {
                    sh "docker build -t jackocodes/demo-repo:${env.IMAGE_NAME} ."
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh "docker push jackocodes/demo-repo:${env.IMAGE_NAME}"
                }
            }
        }
        stage("Commit version update") {
            steps {
                script {
                    withCredentials([string(credentialsId: 'jenkins-commit-token', variable: 'TOKEN')]) {
                        sh 'git config --global user.email "jenkins@example.com"'
                        sh 'git config --global user.name "jenkins"'

                        sh 'git status'
                        sh 'git branch'
                        sh 'git config --list'

                        sh "git remote set-url origin https://oauth2:${TOKEN}@gitlab.com/jackoCodes/jenkins-exercise.git"
                        sh 'git add .'
                        sh 'git commit -m "ci: version bump"'
                        sh 'git push origin HEAD:master'
                    }
                }
            }
        }
    }
}
```

## Exercise 3

```bash
ssh root@165.22.93.244
docker login
docker run -p 3000:3000 jackocodes/demo-repo:1.0
```

## Exercise 4

*Docker.groovy*

```
#!/user/bin/env groovy

package com.example

class Docker implements Serializable {

    def script

    Docker(script) {
        this.script = script
    }

    def buildDockerImage(String imageName) {
        script.echo "Building the docker image"
            script.sh "docker build -t jackocodes/demo-repo:${env.IMAGE_NAME} ."
    }

    def dockerLogin() {
        script.withCredentials(
                [script.usernamePassword(credentialsId: 'docker', usernameVariable: 'USER', passwordVariable: 'PASS')]
        ) {
            script.sh "echo '${script.PASS}' | docker login -u '${script.USER}' --password-stdin"
        }
    }

    def dockerPush(String imageName) {
        script.sh "docker push jackocodes/demo-repo:${env.IMAGE_NAME}"
    }
}
```

*buildImage.groovy*

```
#!/user/bin/env groovy

import com.example.Docker

def call(String imageName) {
    return new Docker(this).buildDockerImage(imageName)
}
```

*buildPackage.groovy*

```
#!/user/bin/env groovy

def call() {
    echo "Building the application for $BRANCH_NAME"
    sh "npm install"
    sh "npm pack"
}
```

*dockerLogin.groovy*

```
#!/user/bin/env groovy

import com.example.Docker

def call() {
    return new Docker(this).dockerLogin()
}
```

*dockerPush.groovy*
```
#!/user/bin/env groovy

import com.example.Docker

def call(String imageName) {
    return new Docker(this).dockerPush(imageName)
}
```

**Jenkinsfile**

```
#!/user/bin/env groovy

// @Library('jenkins-shared-library')  // in case the next command is 'pipeline' a '_' at the end of this line needs to be added
library identifier: "jenkins-shared-library@master", retriever: modernSCM(
    [
        $class: "GitSCMSource",
        remote: "https://gitlab.com/jackoCodes/jenkins-shared-library.git",
        credentialsId: "gitlab-example-code"
    ]
)

def gv

pipeline {
    agent any
    tools {
        maven "maven"
    }
    stages {
        stage("init") {
            steps {
                script {
                    gv = load "script.groovy"
                }
            }
        }
        stage("build jar") {
            steps {
                script {
                    buildJar()
                }
            }
        }
        stage("build and push image") {
            steps {
                script {
                    buildImage 'jackocodes/demo-repo:1.0'
                    dockerLogin()
                    dockerPush 'jackocodes/demo-repo:1.0'
                }
            }
        }
        stage("deploy") {
            steps {
                script {
                    gv.deployApp()
                }
            }
        }
    }
}
```
