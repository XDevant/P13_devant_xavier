# syntax=docker/dockerfile:1

FROM python:3.10-alpine3.16

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUMBUFFERED 1

RUN adduser --disabled-password circleci

USER circleci

COPY ./oc-lettings home/circleci/oc-lettings
WORKDIR /home/circlecioc-lettings

RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    pip install -r requirements.txt && \
    apk del .tmp-deps && \
    chmod -R +x init.sh

EXPOSE $PORT

CMD ./init.sh && gunicorn oc-lettings.wsgi:application --bind $PORT
