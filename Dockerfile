# syntax=docker/dockerfile:1

FROM python:3.10-alpine3.16

ENV PYTHONNUMBUFFERED 1

COPY ./requirements.txt ./requirements.txt
COPY ./db.json ./db.json
COPY ./oc-lettings oc-lettings
WORKDIR /oc-lettings

RUN python -m venv venv
ENV VIRTUAL_ENV /venv \
    PATH /venv/bin:$PATH

RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    chown -R app .

EXPOSE 8000

USER app

CMD [ "pyton", "manage.py", "runserver", "8000" ]
