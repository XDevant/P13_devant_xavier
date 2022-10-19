# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster


COPY requirements.txt requirements.txt

COPY . /app

