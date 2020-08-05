FROM python:3.7-alpine
MAINTAINER Basel H. Ashour

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /api-site
WORKDIR /api-site
COPY ./api-site /api-site

RUN adduser -D dockeruser
USER dockeruser