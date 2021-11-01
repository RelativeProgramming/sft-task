FROM python:3.9.5-alpine3.13

WORKDIR /client

RUN apk add gcc musl-dev mariadb-connector-c-dev

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY writer.py .
