# syntax=docker/dockerfile:1

FROM python:3.9.10-alpine3.14
# FROM python:3.9.16

EXPOSE 5000

WORKDIR /movatic-api

# COPY requirements.txt /movatic-api/requirements.txt

COPY . .

# RUN apt-get update -yqq \
#     && apt-get install -yqq postgresql \
#     && apt-get install -yqq libpq-dev \
#     && apt-get install -yqq gcc

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ENV FLASK_APP=app
# ENV DATABASEURL=
CMD ["python","app.py"]