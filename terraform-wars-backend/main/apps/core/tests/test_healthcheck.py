from http import HTTPStatus

from django.test import Client


def test_healthcheck(client: Client):
    response = client.get("/healthcheck/")
    assert response.status_code == HTTPStatus.OK
