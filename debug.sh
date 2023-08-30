


docker stop $(docker ps -a -q)
docker rmi -f chat-app
docker build -t chat-app .
docker run -d -p 5000:5000 chat-app