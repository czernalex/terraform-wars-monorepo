.PHONY: prepare
prepare:
	python manage.py collectstatic --noinput
	python manage.py compress
	python manage.py migrate

.PHONY: dev
dev:
	python manage.py runserver
