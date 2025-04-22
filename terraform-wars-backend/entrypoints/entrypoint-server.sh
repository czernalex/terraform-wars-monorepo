#!/bin/bash -eu

python manage.py collectstatic --noinput --clear
# python manage.py compilemessages
python manage.py migrate

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8080}

gunicorn main.wsgi --preload --workers=${1:-2} --threads=${2:-4} --worker-class=${3:-gthread} --timeout 300 -b ${HOST}:${PORT} --log-level=info
