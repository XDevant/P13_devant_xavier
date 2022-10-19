# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster


COPY requirements.txt requirements.txt

COPY . /app

WORKDIR /app

pip install -r requirements.txt --user

[CMD]: [ "manage.py", "runserver", "8000"]
