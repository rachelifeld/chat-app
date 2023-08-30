# set base image (host OS)
FROM python:3.8-slim

RUN update-ca-certificates
# set the working directory in the container
WORKDIR /code
# copy the dependencies file to the working directory
COPY requirements.txt .
# install dependencies
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
RUN apt-get update && apt-get install -y \
curl

# copy the content of the local src directory to the working directory
COPY / .
EXPOSE 5000
# command to run on container start
ENV FLASK_ENV development
ENV ROOMS_FILES_PATH rooms/

HEALTHCHECK --interval=10s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1

CMD [ "python", "./chatApp.py" ]

