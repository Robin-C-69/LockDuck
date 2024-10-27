#!/bin/bash

# Define variables
TAG="0.1"
IMAGE_NAME="lockduck-img:$TAG"

# Check if the image already exists
if ! docker images --format '{{.Repository}}:{{.Tag}}' | grep -q "$IMAGE_NAME"; then
    echo "Image $IMAGE_NAME not found. Building the image..."
    docker build -t "$IMAGE_NAME" .
else
    echo "Image $IMAGE_NAME already exists. Skipping build."
fi

# Run the container
clear
docker run -it "$IMAGE_NAME"
