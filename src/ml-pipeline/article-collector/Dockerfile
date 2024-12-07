FROM python:3.11-slim-buster

ENV PYENV_SHELL=/bin/bash

RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential git ffmpeg && \
    pip install --no-cache-dir --upgrade pip && \
    pip install pipenv && \
    mkdir -p /app

WORKDIR /app

ADD Pipfile Pipfile.lock /app/

RUN pipenv sync

ADD . /app

# Entry point
ENTRYPOINT ["/bin/bash", "./docker-entrypoint.sh"]
