docker stop $(docker ps -a -q)
docker rmi -f chat-app