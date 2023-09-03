FROM python:3.10-slim

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential && \
    pip install -r requirements.txt

COPY . /app

