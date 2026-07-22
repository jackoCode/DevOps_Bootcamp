#!/bin/bash

# Update package lists
sudo apt update

# Find the latest available OpenJDK JDK package
LATEST_JDK=$(apt-cache search '^openjdk-[0-9]+-jdk$' | awk '{print $1}' | sort -V | tail -n 1)

# Check if a package was found
if [ -z "$LATEST_JDK" ]; then
    echo "No OpenJDK JDK package found in the repositories."
    exit 1
fi

echo "Installing $LATEST_JDK..."

# Install the latest JDK
sudo apt install -y "$LATEST_JDK"

# Display the installed Java version
echo
echo "Java installation complete."
java -version
javac -version
