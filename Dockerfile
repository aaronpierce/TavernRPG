# syntax=docker/dockerfile:1

FROM python:3.10.7-buster

WORKDIR /app

COPY . .

CMD [ "python3", "server/app.py"]
