#!/bin/bash

# Setting the project dir
ROOT_DIR="/root/skittens"
PROJECT_DIR="$ROOT_DIR/fsp-pro"
DEPLOYMENTS_DIR="$PROJECT_DIR/deployments"
ORIGIN="https://github.com/thatusualguy/fsp-pro"

echo "Clonning a repo if it doesn't exists"
if [ ! -f "$PROJECT_DIR"]; then
    cd "$ROOT_DIR" && git clone "$ORIGIN"
    echo "Successfully cloned from $ORIGIN"
fi

if [ ! -f "$PROJECT_DIR/.env"]; then
    echo "Error: .env file not found in $PROJECT_DIR at the server."
    exit 1
fi

echo "Exporting .env into the current shell..."
export $(grep -v "^#" "$PROJECT_DIR/.env" | xargs)
echo ".env file exported."

echo "Pulling a repo..."
cd "$PROJECT_DIR" && git stash && git fetch origin "$BRANCH_NAME" && git reset --hard origin/"$BRANCH_NAME"
echo "Pulled successfully."

if ! docker network ls --format "{{.Name}}" | grep -q "^russian_cup_backend_net"; then
    docker network create -d bridge russian_cup_backend_net
    echo "Creating russian_cup_backend_net network for fsp-pro project"
fi

echo "Stopping the existing containers"
cd "$DEPLOYMENTS_DIR" && docker compose -f docker-compose.yml down

echo "Waiting for services to be removed..."
while [ "$(docker ps --filter "name=russian-cup-backend" -q | wc -l)" -ne 0 ]; do
    sleep 1
done
echo "All russian_cup_backend containers removed."

echo "Deploying the service..."
cd "$DEPLOYMENTS_DIR" && docker compose -f docker-compose.yml up --build
echo "Deployment completed."



