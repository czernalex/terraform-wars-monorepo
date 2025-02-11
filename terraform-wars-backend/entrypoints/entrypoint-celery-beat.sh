#! /bin/bash -eu

celery --app=main.celeryconf beat --loglevel=INFO
