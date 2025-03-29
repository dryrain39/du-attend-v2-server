FROM python:3.9-alpine

# install build-base(gcc) for uvicorn

COPY requirements.txt /app/requirements.txt

RUN apk add postgresql-libs gcc libc-dev

RUN apk add --no-cache --virtual .build-deps musl-dev libffi-dev postgresql-dev alpine-sdk \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apk del .build-deps

COPY . /app/

WORKDIR /app
RUN chmod +x /app/entry.sh
ENTRYPOINT /app/entry.sh
