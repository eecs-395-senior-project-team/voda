FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev\
    && apk add postgresql-dev postgresql-client \
    && apk add libffi-dev \
    && apk add libxslt-dev

WORKDIR /app

COPY . /app

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/production.txt