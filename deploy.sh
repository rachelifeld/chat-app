#!/bin/bash

#set -e to enable error handling, so if any of the commands fail, it will exit immediately. This helps to ensure that the deployment process is halted if any issues occur.
set -e

# Prompt user for version and commit hash
read -p "Enter the version: " version
read -p "Enter the commit hash: " commit_hash

git tag "$version" "$commit_hash" || echo "Failed to tag the commit"

# Build the image
docker build -t chat-app:$version . || echo "Failed to build the image"

#push the tag to github repository
git push origin "$version" || echo "failed to push to github"

echo "Deployment successful!"

