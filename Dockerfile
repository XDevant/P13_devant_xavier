# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

COPY requirements.txt requirements.txt

COPY . /app

WORKDIR /app
RUN python -m venv /py
RUN /py/bin/pip install --upgrade pip
RUN /py/bin/pip install -r /requirements.txt
RUN adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"

USER django-user

CMD [ "manage.py", "runserver", "8000"]
