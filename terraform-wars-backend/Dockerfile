FROM python:3.13-slim

RUN apt-get update && apt-get install -y curl

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

RUN mkdir /app

RUN groupadd --gid 1000 app && useradd --uid 1000 --gid 1000 -m app

WORKDIR /app

ADD --chown=app:app . /app/

RUN chmod +x /app/entrypoints/entrypoint-server.sh

RUN pip install poetry==2.0.1

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi --no-cache --only main

USER app

EXPOSE $PORT
