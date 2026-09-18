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
ssh root@<droplet IP address>
docker login
docker run -p 3000:3000 <docker-hub-id>/demo-repo:<image-name>
```

## Exercise 4

