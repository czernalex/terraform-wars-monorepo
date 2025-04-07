from http import HTTPStatus

from django.conf import settings
from django.test import Client
from django.urls import reverse


class TestApiAuthRouter:
    def test_get_csrf_token_response_contains_csrf_cookie(self, client: Client):
        response = client.post(reverse("terraform-wars-api:csrf"))
        assert response.status_code == HTTPStatus.NO_CONTENT
        assert response.cookies.get(settings.CSRF_COOKIE_NAME) is not None
