FROM python:3.7-alpine
LABEL maintainer="Basel H. Ashour"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client \
    jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    musl-dev zlib zlib-dev
RUN pip install -r requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /api-site
WORKDIR /api-site
COPY ./api-site /api-site

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D dockeruser
RUN chown -R dockeruser:dockeruser /vol/
RUN chmod -R 755 /vol/web
USER dockeruser