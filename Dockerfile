# pull official base image
#FROM python:3.9.6-alpine
FROM python:3.9

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
#RUN apk update \
#    && apk add postgresql-dev gcc python3-dev musl-dev


# install dependencies
RUN pip install --upgrade pip
RUN pip install -U pip setuptools wheel ruamel.yaml.clib==0.2.6
RUN pip install -U pip setuptools wheel psycopg2==2.9.2
RUN pip install -U pip setuptools wheel psycopg2-binary==2.8.5
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY ./Irangard .
