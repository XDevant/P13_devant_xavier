# syntax=docker/dockerfile:1

FROM python:3.10-alpine3.16

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUMBUFFERED 1

COPY ./oc-lettings ./oc-lettings
WORKDIR /oc-lettings


RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    pip install -r requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password CircleCI && \
    chown -R home/CircleCI .  && \
    chown -R . .


EXPOSE $PORT

ENV PATH=/venv/bin:$PATH

USER CircleCI

CMD python manage.py init && gunicorn oc-lettings.wsgi:application --bind $PORT
