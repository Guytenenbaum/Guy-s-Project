FROM python:3.10-slim

WORKDIR /guyproject

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install Django psycopg2-binary

COPY . .

CMD python manage.py runserver 0.0.0.0:8000