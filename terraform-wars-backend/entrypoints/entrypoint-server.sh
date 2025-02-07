#!/bin/bash

python manage.py collectstatic --noinput --clear
python manage.py compilemessages
python manage.py migrate

gunicorn main.wsgi --preload --workers=${1:-2} --threads=${2:-4} --worker-class=${3:-gthread} --timeout 300 -b 0.0.0.0:8888 --log-level=info
