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


### Exercise 4 - Bash Script - User Processes Sorted


### Exercise 5 - Bash Script - Number of User Processes Sorted


### Exercise 6 - Bash Script - Start Node App


### Exercise 7 - Bash Script - Node App Check Status


### Exercise 8 - Bash Script - Node App with Log Directory


### Exercise 9 - Bash Script - Node App with Service user