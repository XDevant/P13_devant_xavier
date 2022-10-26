# syntax=docker/dockerfile:1

FROM python:3.10-alpine3.16

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUMBUFFERED 1

COPY ./oc-lettings oc-lettings
WORKDIR /oc-lettings

RUN python -m venv venv && . venv/bin/activate
ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH

RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    pip install -r requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home circleci && \
    chown -R app .

EXPOSE $PORT

USER circleci

CMD ./init.sh && gunicorn oc-lettings.wsgi:application --bind $PORT
