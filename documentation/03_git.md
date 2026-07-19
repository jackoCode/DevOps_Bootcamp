# Version Control with Git

## Gitlab/Github

- Working with Git in stages
  - Working directory
  - Staging area
  - Local repository
  - Remote repository

| Git command                        | Info                                                                                         |
|------------------------------------|----------------------------------------------------------------------------------------------|
| git status                         | Current status of the local repository                                                       |
| git add *filename*                 | Add file to the staging area                                                                 |
| git add .                          | Add all files to the staging area                                                            |
| git commit                         | Commit file and add commit message using Vim                                                 |
| git commit -m "..."                | Commit file and add commit message after -m                                                  |
| git push                           | Push changes to remote                                                                       |
| git init                           | Initialize an empty Git repository                                                           |
| git remote add origin git@repo-URL | Connect a local repository to remote <br> Use "git push --set-upstream origin master" before |

## Branches

- Best practice for naming branches
  - For feature branches use "feature/..."
  - For bugfixes use "bugfix/..."

| Git command                   | Info                                                                                                                             |
|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| git branch                    | Shows all loacal branches                                                                                                        |
| git pull                      | Updates the local branch                                                                                                         |
| git checkout *branch-name*    | Checkout a branch                                                                                                                |
| git checkout -b *branch-name* | Creates a new branch and checks it out <br> To push this new branch to remote use "git push --set-upstream origin *branch-name*" |

- Develop branch
  - intermediary master
  - during sprints for features and/or bugfixes
  - merge into master at the end of the sprint

- Trank based vs. Feature based
  - Trunk based is the best practice for DevOps and CI/CD

## Merge requests

The terms "pull request" and "merge request" mean basically the same. The terms are different used in different tool and teams.

## Deleting Branches

- After a branch was merged the best way is to delete this branch. Therefore, there are no old branches with unknown status.
- Delete a branch with "git branch -d *branch-name*"

## Rebase

**First option**

| Git command | Info                                                              |
|-------------|-------------------------------------------------------------------|
| git pull    | Update the local branch                                           |
| git push    | Push all changes to remote (incl. the pulled changes from remote) |

**Second option**

| Git command | Info                                                    |
|-------------|---------------------------------------------------------|
| git pull -r | Rebase; this stacks the loacal changes on top of remote |
| git push    | Push all changes to remote                              |

## Merch conflicts

This happens if local and remote are changed at the same point (e.g. the same line in the code). This means a merge is 
no longer possible because there is no way to know what change should be implemented. This problem needs to be
resolved manually (after talking to the other person).

If the conflict is resolved:
1. git rebase --continue
2. git push

## .gitignore

Excluding files and folders from pushing to remote.

If something was already pushed to the remote repository and later added to .gitignore then this file(s)/folder(s) 
are shown as changed if "git status" is executed. <br> To fix this:
1. git rm -r --cached . (instead of "." an actual file/folder name can be given)
2. git add .
3. git commit
4. git push

## Git stash

| Git command   | Info                     |
|---------------|--------------------------|
| git stash     | Save changes for later   |
| git stash pop | Get stashed changes back |

**Use cases**
1. Stash before change branches to save the changes of the current branch for later
2. Hide changes temporarily to test if the code works without this changes

## Back in history

| Git command                | Info                                                                                                                                                 |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| git log                    | Show the change history. Every commit has its own hash value.                                                                                        |
| git checkout *hashvalue*   | Going back to the commit of this hash. It would be possible to make changes now and create a new branch, but this is not realy a realistic scenario. |
| git checkout *branch-name* | Go back to the latest version of the branch.                                                                                                         |

## Undoing commits

| Git command             | Info                                                                                                                   |
|-------------------------|------------------------------------------------------------------------------------------------------------------------|
| git reset --hard HEAD~1 | Reset the last commit. "--hard" will discard all changes.                                                              |
| git reset --soft HEAD~1 | With "--soft" the changes will not be discarded. This is the default. Therefore, "--soft" is not explicitly necessary. |
| git commit --amend      | Add changes to the last commit                                                                                         |

If a commit is already push to remote then
1. git reset --hard HEAD~1
2. git push --force <br> Without "--force" a push would not be possible because remote has the newer version.

**CAUTION**<br>
Do not do this to *main* branch or to repositories where other people also working in.

**Alternative**<br>
"git revert *hash*" does not overwrite the changes but creates a new commit.

## Merging branches

| Git command        | Info                                                                                                 |
|--------------------|------------------------------------------------------------------------------------------------------|
| git merge *master* | Merch changes from *master* into the current branch (the loacal *master* needs to be updated first). |

## Git for DevOps

- Infrastructure as Code
- CI/CD and build automation

## Git cheat sheet

[atlassian-git-cheatsheet.pdf](media/atlassian-git-cheatsheet.pdf)