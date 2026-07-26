#!/usr/bin/env bash

set -euo pipefail

ARTIFACT_URL="https://node-envvars-artifact.s3.eu-west-2.amazonaws.com/bootcamp-node-envvars-project-1.0.0.tgz"
ARTIFACT_NAME="bootcamp-node-envvars-project-1.0.0.tgz"

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

export APP_ENV="dev"
export DB_USER="myuser"
export DB_PWD="mysecret"
export LOG_DIR

echo "Setting permissions"
sudo chown -R "$APP_USER:$APP_USER" "$APP_DIR"
sudo chown -R "$APP_USER:$APP_USER" "$LOG_DIR"

echo "Installing npm dependencies as $APP_USER"
sudo -u "$APP_USER" bash <<EOF

cd "$(pwd)/$APP_DIR"

export APP_ENV="$APP_ENV"
export DB_USER="$DB_USER"
export DB_PWD="$DB_PWD"
export LOG_DIR="$LOG_DIR"

npm install
EOF

echo "Starting application as $APP_USER..."

sudo -u "$APP_USER" bash <<EOF &

cd "$(pwd)/$APP_DIR"

export APP_ENV="$APP_ENV"
export DB_USER="$DB_USER"
export DB_PWD="$DB_PWD"
export LOG_DIR="$LOG_DIR"

nohup node server.js > server.log 2>&1 &
echo \$! > app.pid
EOF

echo "Waiting for application to start"
sleep 5  # Wait to make sure the app is running

APP_PID=$(cat "$APP_DIR/app.pid")

if ps -p "$APP_PID" > /dev/null; then
    echo
    echo "Application started successfully!"
    echo

    echo "Process information:"
    ps -fp "$APP_PID"

    PORT=$(ss -ltnp 2>/dev/null | grep "$APP_PID" | awk '{print $4}' | awk -F: '{print $NF}' | head -1)

    if [ -n "$PORT" ]; then
        echo
        echo "Application is listening on port: $PORT"
    else
        echo
        echo "Application is running, but listening port could not be determined."
    fi

    echo
    echo "Application log:"
    echo "----------------------------------------"

    if [ -f "$LOG_DIR/app.log" ]; then
        cat "$LOG_DIR/app.log"
    else
        echo "app.log not found in $LOG_DIR"
    fi

    echo "----------------------------------------"

else
    echo
    echo "Application failed to start."
    echo
    echo "Server output:"
    cat server.log
    exit 1
fi