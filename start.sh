#!/bin/bash

# Define variables
CONTAINER_NAME="lockduck"
TAG="0.1"
IMAGE_NAME="lockduck-img:$TAG"
VOLUME_NAME="lockduck_db"
VOLUME_MOUNT_PATH="/mnt"

# Check if the image already exists
if ! docker images --format '{{.Repository}}:{{.Tag}}' | grep "$IMAGE_NAME"; then
    echo "Image $IMAGE_NAME not found. Building the image..."
    if ! docker build -t "$IMAGE_NAME" .; then
        echo "Failed to build the image."
        exit 1
    fi
else
    echo "Image $IMAGE_NAME already exists. Skipping build."
fi

# Check if volume exists
VOLUME_EXISTS=$(docker volume ls --filter name=$VOLUME_NAME -q)

# Create the volume if it doesn't exist
if [ -z "$VOLUME_EXISTS" ]; then
    echo "Volume $VOLUME_NAME does not exist. Creating it..."
    docker volume create $VOLUME_NAME
else
    echo "Volume $VOLUME_NAME already exists. Skipping creation."
fi

# Run the container
CONTAINER_EXISTS=$(docker ps -a --filter "name=$CONTAINER_NAME" -q)

printf "\033[2J\033[H"
if [ -z "$CONTAINER_EXISTS" ]; then
    docker run -it -v $VOLUME_NAME:$VOLUME_MOUNT_PATH --name $CONTAINER_NAME "$IMAGE_NAME"
else
    docker container start -i $CONTAINER_NAME
fi
