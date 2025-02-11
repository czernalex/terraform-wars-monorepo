#! /bin/bash -eu

celery --app=main.celeryconf worker --loglevel=INFO
