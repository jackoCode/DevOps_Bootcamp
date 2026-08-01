# Exercise - Version control with GIT

## Exercise 1 - Clone and create new repository

Clone the repository
```
git clone https://gitlab.com/twn-devops-bootcamp/latest/03-git/git-exercises.git
```

Change directory (project folder)
```
cd git-exercises
```

Check current remote
```
git remote -v
```

Change current remote to my remote
```
git remote set-url origin git@github.com:jackoCode/DevOps_Bootcamp_Exercise.git
```

Push everything to my repository
```
git push -u origin main
```

## Exercise 2 - .gitignore

Remove from Git cache
```
git rm -r --cached .
git add .
git commit -m "..."
git push
```
Add .gitignore file
```
touch .gitignore
vim .gitignore
git add .
git commit -m "added .gitignore file"
git push
```

## Exercise 3 - Feature branch

Create new feature branch and checkout
```
git checkout -b feature/upgrade_and_add
```

Check changes
```
git diff
```

Commit changes
```
git add .
git commit -m "Updated logstash-logback-encoder version to 7.3 and added image to index.html"
```

Push
```
git push --set-upstream origin featue/upgrade_and_add
git push
```

## Exercise 4 - Bugfix branch

Create new bugfix branch and checkout
```
git checkout -b bugfix/spelling_error
```

Correct the typo
```
vim Application.java
```

Check changes
```
git diff
```

Commit changes
```
git add .
git commit -m "Fixed spelling error 'starte' -> 'started'"
```

Push
```
git push --set-upstream origin bugfix/spelling_error
git push
```


## Exercise 5 - Merge request

![merge_request_feature_branch_gitlab.png](../../media/pics/exercises/03_version_control_git/merge_request_feature_branch_gitlab.png)

## Exercise 6 - Fix merge conflict

Update logstash-logback-encoder version
```
vim build.gradle
```

Commit and push to remote
```
git add .
git commit -m "Updated logstash-logback-encoder version from 5.2 to 7.2"
git push
```

Resolve merge request
```
git fetch origin
git merge origin/main
-> MERGE CONFLICT <-
vim build.gradle
git add .
git commit -m "resolved merge conflict"
git push
```

## Exercise 7 - Revert commit

Correct spelling error und update image URL (both changes are done in separate commits)
```
vim index.html
```

Commit changes and push to remote
```
git add .
git commit -m "..."
git push
```

Revert the last commit
```
git reset --hard <commit hash>
git push --force
```

## Exercise 8 - Reset commit

After change and commit
```
git reset --hard HEAD~1
```

## Exercise 9 - Merge

```
git checkout master
git pull origin master
git merge bugfix-branch
git push origin master
```

## Exercise 10 - Delete branch

```
git branch -d <branch name>
```