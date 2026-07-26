#!/bin/bash

# Update package lists
sudo apt update

# Find the latest available OpenJDK JDK package
LATEST_JDK=$(apt-cache search '^openjdk-[0-9]+-jdk$' | awk '{print $1}' | sort -V | tail -n 1)

# Check if a package was found
if [ -z "$LATEST_JDK" ];
then
  echo "No OpenJDK JDK package found in the repositories."
  exit 1
fi

# Install the latest JDK
echo "Installing $LATEST_JDK..."
sudo apt install -y "$LATEST_JDK"

# Display the installed Java version
echo
echo "Java installation complete."
java -version
javac -version

# Check whether Java is installed
if ! command -v java >/dev/null 2>&1;
then
  echo "Java is NOT installed."
  exit 1
else
  echo "Java is installed."
fi

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