# syntax=docker/dockerfile:1

FROM python:3.10-alpine3.16

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUMBUFFERED 1

COPY ./oc_lettings ./oc_lettings
WORKDIR ./oc_lettings

RUN python -m venv /py && \
    . /py/bin/activate && \
    pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    pip install -r requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password -H app && \
    chown -R app . && \
    chown -R app /etc/profile && \
    chmod 777 /etc/profile

EXPOSE $PORT

ENV PATH=/py/bin:/etc/profile:$PATH
ENV PYTHONPATH="./oc_lettings::$PYTHONPATH"

USER app

CMD python -m manage.py init && gunicorn --env DJANGO_SETTINGS_MODULE=oc_lettings.settings oc_lettings.wsgi:application --bind 0.0.0.0:$PORT
