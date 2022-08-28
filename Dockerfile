FROM python:3.8-alpine

# install build-base(gcc) for uvicorn

COPY requirements.txt /app/requirements.txt

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apk del .build-deps

COPY . /app/

WORKDIR /app
RUN chmod +x /app/entry.sh
ENTRYPOINT /app/entry.sh
