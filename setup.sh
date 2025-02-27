#!/bin/bash

# Define the repository and folder path
repo_url="https://github.com/Tahl0s/jigsaw-unified-deployment-engine.git"
repo_dir="jigsaw-unified-deployment-engine"

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed. Install it and try again."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Install it and try again."
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "Error: Docker daemon is not running."
    exit 1
fi

# Clone or update repository
if [ ! -d "$repo_dir" ]; then
    echo "Cloning the repository..."
    git clone "$repo_url"
else
    echo "Repository already exists. Pulling latest changes..."
    cd "$repo_dir" || exit
    git pull
    cd ..
fi

# Check if docker-compose.yml exists
if [ ! -f "$repo_dir/docker-compose.yml" ]; then
    echo "Error: docker-compose.yml is missing in the repo!"
    exit 1
fi

# Move into the repository folder
cd "$repo_dir" || exit

# Build and start the Docker containers
echo "Starting Docker Compose..."
docker-compose up -d --build
