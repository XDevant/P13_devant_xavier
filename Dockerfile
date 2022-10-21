# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster


COPY ./requirements.txt /requirements.txt
RUN mkdir /oc-lettings
COPY ./oc-lettings oc-lettings
WORKDIR /oc-lettings

RUN python -m venv venv
ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

EXPOSE 8000

CMD [ "pyton", "manage.py", "runserver", "8000" ]
