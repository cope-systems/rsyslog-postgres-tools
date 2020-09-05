FROM python:3.8-slim-buster
RUN apt-get -y update && apt-get -y upgrade

COPY . /app
RUN python3 -m pip install -r /app/requirements.txt
