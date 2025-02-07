.PHONY: prepare
prepare:
	python manage.py collectstatic --noinput
	python manage.py compress
	python manage.py migrate

.PHONY: dev
dev:
	python manage.py runserver

.PHONY: test
test:
	python manage.py test --no-input --keep-db --settings=main.settings.testing
