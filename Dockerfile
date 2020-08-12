FROM python:3.7-alpine
LABEL maintainer="Basel H. Ashour"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /api-site
WORKDIR /api-site
COPY ./api-site /api-site

RUN adduser -D dockeruser
USER dockeruser