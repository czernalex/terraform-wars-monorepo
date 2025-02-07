FROM python:3.13-slim

RUN apt-get update && apt-get install -y curl

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

RUN mkdir /app

RUN groupadd --gid 1000 app && useradd --uid 1000 --gid 1000 -m app

WORKDIR /app

ADD --chown=app:app . /app/

RUN chmod +x /app/entrypoints/entrypoint-server.sh

RUN pip install poetry==1.5.1

RUN poetry export --only main --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt
RUN pip install --force-reinstall -r requirements.txt

USER app
