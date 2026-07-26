#!/bin/bash

set -euo pipefail

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
    echo "Neither curl nor wget is installed."
    exit 1
fi

echo "Unzip artifact"
tar -xzf "$ARTIFACT_NAME"
APP_DIR=$(tar -tzf "$ARTIFACT_NAME" | head -1 | cut -d/ -f1)

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

echo "---------------------"
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