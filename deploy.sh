#!/bin/bash

# Prompt user for version and commit hash
read -p "Enter the version: " version
read -p "Enter the commit hash: " commit_hash

git tag "$version" "$commit_hash" || { echo "Failed to tag the commit"; exit 1; }

# Build the image with a tag
docker build -t chat-app:"$version" . || { echo "Failed to build the image"; exit 1; }

# Tag the image for your registry 
docker tag chat-app:"$version" rivkarizel/chat-app:"$version" || { echo "Failed to tag for registry"; exit 1; }

# Push the image to the registry 
docker push rivkarizel/chat-app:"$version" || { echo "Failed to push to registry"; exit 1; }

# Push the tag to the GitHub repository
git push origin "$version" || { echo "Failed to push to GitHub"; exit 1; }

echo "Deployment successful!"
