FROM python:3.10-slim-buster

WORKDIR /app
COPY requirements.txt ./requirements.txt
COPY manage.py ./manage.py
COPY oc_lettings ./oc_lettings
COPY oc_lettings_site ./oc_lettings_site
COPY lettings ./lettings
COPY profiles ./profiles

CMD [ "python", "-m", "venv"]
CMD [ "pip"," install", "--upgrade", "pip" ]
CMD ["pip", "install", "-r", "requirements.txt"]

CMD [ "python", "-m", " manage", "runserver", "8000"]