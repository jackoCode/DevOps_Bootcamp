# Exercise - OS and Linux

### Exercise 1 - Linux Mint VM

| Topic                            |        |
|----------------------------------|--------|
| Package Manager                  |        |
| CLI editor                       |        |
| Software center/software manager |        |
| Shell                            |        |

### Exercise 2 - Bash Script - Install Java

```bash
#!/bin/bash

# Update package lists<br>
sudo apt update

# Find the latest available OpenJDK JDK package
LATEST_JDK=$(apt-cache search openjdk | awk '{print $1}' | grep '^openjdk-[0-9]\+-jdk$' | sort -V | tail -n 1)
```

| Command               | Info                                                                                                                                                                                                       |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| apt-cache search      | Returns the search as plain text (better to parse)                                                                                                                                                         |
| awk '{print $1}'      | *awk* is used for processing and analyzing text files. It reads input line by line, splits each line into fields (columns), and lets you perform actions on those fields. *$1* refers to the first column. |
| ^openjdk-[0-9]\+-jdk$ | *^* begin of the regex, *[0-9]\+* one or more digits from 0 to 9, *$* end of regex                                                                                                                         |
| sort -V               | Version-aware sort                                                                                                                                                                                         |
| tail -n 1             | Returns the last line                                                                                                                                                                                      |

```bash
# Check if a package was found
if [ -z "$LATEST_JDK" ]; then
    echo "No OpenJDK JDK package found in the repositories."
    exit 1
fi
```
| Command              | Info                                        |
|----------------------|---------------------------------------------|
| [ -z "$LATEST_JDK" ] | Checks if the length of the string is zero. |


```bash
echo "Installing $LATEST_JDK..."

# Install the latest JDK
sudo apt install -y "$LATEST_JDK"
```

| Command        | Info                                  |
|----------------|---------------------------------------|
| apt install -y | Install package and answer YES (*-y*) |


```bash
# Display the installed Java version
echo
echo "Java installation complete."
java -version
javac -version
```

| Command        | Info                       |
|----------------|----------------------------|
| java -version  | Java runtime (JVM) version |
| javac -version | Java compiler version      |

```bash
# Check whether Java is installed
if ! command -v java >/dev/null 2>&1;
then
  echo "Java is NOT installed."
  exit 1
else
  echo "Java is installed."
fi
```

| Command         | Info                                                        |
|-----------------|-------------------------------------------------------------|
| !               | NOT                                                         |
| command -v java | Calls command "java". *-v* for verbose.                     |
| >/dev/null      | Discard the output                                          |
| 2>&1            | Send standard output and also standard error to */dev/null* |


```bash
# Extract major version number
VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
MAJOR=$(echo "$VERSION" | awk -F. '{if ($1 == "1") print $2; else print $1}')

# Check if Java version is lower than 11
if [ "$MAJOR" -lt 11 ]; then
  echo "An older Java version is installed (Java $MAJOR)."
  echo "Java 11 or higher is NOT available."
  echo "Installation was NOT successful."
else
  echo "No older Java version detected."
  echo "Java 11 or higher is installed (Java $MAJOR)."
  echo "Installation was successful."
fi
```

| Command | Info                  |
|---------|-----------------------|
| awk -F. | *-F.* separat by "."  |

### Exercise 3 - Bash Script - User Processes

```bash
#!/bin/bash

echo "Get all running processes for user '$USER'"
ps aux | grep $USER
```

| Command    | Info                        |
|------------|-----------------------------|
| ps aux     | Print all running processes |
| grep $USER | *grep* for current user     |

### Exercise 4 - Bash Script - User Processes Sorted

```bash
#!/bin/bash

read -p "Sort list by memory (m) usage or CPU (c) consumption: " sort_option

echo "Get all running processes of user '$USER'"

if [ "$sort_option" == m ];
then
  echo "Process list sorted by memory usage."
  ps aux --sort=-%mem | grep $USER
elif [ "$sort_option" == c ];
then
  echo "Process list sorted by CPU consumption."
  ps aux --sort=-%cpu | grep $USER
else
  echo "Invalid input. Must be 'm' or 'c'."
fi
```

| Command      | Info                                    |
|--------------|-----------------------------------------|
| --sort=-%mem | Sort by *%mem* in desending ("-") order |

### Exercise 5 - Bash Script - Number of User Processes Sorted

```bash
#!/bin/bash

read -p "Sort list by memory (m) usage or CPU (c) consumption: " sort_option
read -p "Number of processes to print: " no_of_processes

echo "Get all running processes of user '$USER'"

if [ "$sort_option" == m ];
then
  echo "Process list sorted by memory usage."
  ps aux --sort=-%mem | grep $USER | head -n "$no_of_processes"
elif [ "$sort_option" == c ];
then
  echo "Process list sorted by CPU consumption."
  ps aux --sort=-%cpu | grep $USER | head -n "$no_of_processes"
else
  echo "Invalid input. Must be 'm' or 'c'."
fi
```

| Command                    | Info                                                                |
|----------------------------|---------------------------------------------------------------------|
| head -n "$no_of_processes" | Print the given number of processes starting at the top of the list |

### Exercise 6 - Bash Script - Start Node App

```bash
#!/bin/bash

set -euo pipefail
```

| Command           | Info                                              |
|-------------------|---------------------------------------------------|
| set -euo pipefail | *-e*: Exit on command failure                     |
|                   | *-u*: Exit on unset variables                     |
|                   | *-o pipefail*: Pipeline fail if any command fails |

```bash
ARTIFACT_URL="https://node-envvars-artifact.s3.eu-west-2.amazonaws.com/bootcamp-node-envvars-project-1.0.0.tgz"
ARTIFACT_NAME="bootcamp-node-envvars-project-1.0.0.tgz"

echo "Installing Node.js and npm"
sudo apt-get update
sudo apt-get install -y nodejs npm

echo "Installed versions:"
echo "Node.js: $(node -v)"
echo "npm: $(npm -v)"

echo "Downloading artifact"
if command -v curl >/dev/null 2>&1; then
    curl -L -o "$ARTIFACT_NAME" "$ARTIFACT_URL"
elif command -v wget >/dev/null 2>&1; then
    wget -O "$ARTIFACT_NAME" "$ARTIFACT_URL"
else
    echo "Neither curl nor wget are installed."
    exit 1
fi
```

| Command    | Info                                               |
|------------|----------------------------------------------------|
| curl -L -o | *-L*: Follow redirects                             |
|            | *-o*: Save downloaded file with the specified name |
| wget -O    | *-O*: Save downloaded file with the specified name |
|            | NOTE: *wget* will follow redirectes by default     |

```bash
echo "Unzip artifact"
tar -xzf "$ARTIFACT_NAME"
APP_DIR=$(tar -tzf "$ARTIFACT_NAME" | head -1 | cut -d/ -f1)

```

| Command                | Info                                           |
|------------------------|------------------------------------------------|
| tar -xzf               | *-x*: Extract                                  |
|                        | *-z*: gzip-compressed                          |
|                        | *-f*: Specified file                           |
| tar -tzf               | *-t*: List the archive content                 |
| head -1 \| cut -d/ -f1 | *head -1*: Beginning of the input              |
|                        | *cut -d/ -f1*: Split at "/" and get first item |

```bash

echo "Setting environment variables"
export APP_ENV="dev"
export DB_USER="myuser"
export DB_PWD="mysecret"

echo "Changing to app directory"
cd "$APP_DIR"

echo "Installing app dependencies"
npm install

echo "Starting Node.js app (running in the background)"
nohup node server.js > server.log 2>&1 &

echo "Application started successfully."
echo "PID: $!"
echo "Logs: $(pwd)/server.log"
```

### Exercise 7 - Bash Script - Node App Check Status

```bash
echo "Check app is running"
APP_PID=$!
sleep 5

if ps -p "$APP_PID" > /dev/null; then
    echo "Application started successfully."
    echo "Process information:"
    ps -fp "$APP_PID"

    PORT=$(ss -ltnp 2>/dev/null | grep "$APP_PID" | awk '{print $4}' | awk -F: '{print $NF}' | head -1)

    if [ -n "$PORT" ]; then
        echo "Application is listening on port: $PORT"
    else
        echo "Application is running, but no listening port was found."
    fi
else
    echo "Application failed to start."
    echo "Last 20 lines of log:"
    tail -20 server.log
    exit 1
fi
```

### Exercise 8 - Bash Script - Node App with Log Directory

```bash
if [ $# -ne 1 ]; then
    echo "Usage: $0 <log_directory>"
    exit 1
fi

LOG_DIR="$1"

if [ ! -d "$LOG_DIR" ]; then
    echo "Creating log directory: $LOG_DIR"
    mkdir -p "$LOG_DIR"
fi

LOG_DIR=$(cd "$LOG_DIR" && pwd)
```

| Command         | Info                   |
|-----------------|------------------------|
| $# -ne 1        | *$#*: Number of params |
|                 | *-ne*: Not equal       |
| ! -d "$LOG_DIR" | *-d*: Is directory     |


### Exercise 9 - Bash Script - Node App with Service user

```bash
sudo -u "$APP_USER" bash <<EOF

cd "$(pwd)/$APP_DIR"

export APP_ENV="$APP_ENV"
export DB_USER="$DB_USER"
export DB_PWD="$DB_PWD"
export LOG_DIR="$LOG_DIR"

npm install
EOF
```

| Comand        | Info                          |
|---------------|-------------------------------|
| <<EOF ... EOF | Used to write multiple lines. |
