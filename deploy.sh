#!/bin/bash

#set -e to enable error handling, so if any of the commands fail, it will exit immediately. This helps to ensure that the deployment process is halted if any issues occur.
set -e

# Prompt user for version and commit hash
read -p "Enter the version: " version
read -p "Enter the commit hash: " commit_hash

# Set the repository details
repository="your-github-repository"
image_name="my-chat-app"

# Tagging the Docker image
docker tag $image_name:$version $repository:$version-$commit_hash

# Building the Docker image
docker build -t $image_name:$version .

# Tagging the built image with commit hash
docker tag $image_name:$version $repository:$commit_hash

# Pushing the tags to the GitHub repository
docker push $repository:$version-$commit_hash
docker push $repository:$commit_hash


echo "Deployment successful!"