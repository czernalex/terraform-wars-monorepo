from http import HTTPStatus

from allauth.account.models import EmailAddress
from model_bakery import baker

from main.apps.core.utils import ApiClientTestCase


class AllAuthLoginTestCase(ApiClientTestCase):
    def setUp(self):
        super().setUp()
        self.user = baker.make("users.User", email="user@email.com", is_active=True)
        self.user.set_password("Password1")
        self.user.save()
        self.email_address = baker.make(EmailAddress, email=self.user.email, user=self.user, verified=True, primary=True)

    def test_login(self):
        response = self.client.post(
            "/allauth-api/browser/v1/auth/login",
            content_type="application/json",
            data={
                "email": "user@email.com",
                "password": "Password1",
            },
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def test_login_invalid_password(self):
        response = self.client.post(
            "/allauth-api/browser/v1/auth/login",
            content_type="application/json",
            data={
                "email": "user@email.com",
                "password": "InvalidPassword",
            },
        )
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_login_invalid_email(self):
        response = self.client.post(
            "/allauth-api/browser/v1/auth/login",
            content_type="application/json",
            data={
                "email": "nonexisting.email@email.com",
                "password": "Password",
            },
        )
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)


    def test_login_unverified_email_address(self):
        self.email_address.verified = False
        self.email_address.save()
        response = self.client.post(
            "/allauth-api/browser/v1/auth/login",
            content_type="application/json",
            data={
                "email": "user@email.com",
                "password": "Password1",
            },
        )
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(
            "/allauth-api/browser/v1/auth/login",
            content_type="application/json",
            data={
                "email": "user@email.com",
                "password": "Password1",
            },
        )
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)

    def test_repeated_login(self):
        response = self.client.post(
            "/allauth-api/browser/v1/auth/login",
            content_type="application/json",
            data={
                "email": "user@email.com",
                "password": "Password1",
            },
        )
        self.assertEqual(HTTPStatus.OK, response.status_code)
        response = self.client.post(
            "/allauth-api/browser/v1/auth/login",
            content_type="application/json",
            data={
                "email": "user@email.com",
                "password": "Password1",
            },
        )
        self.assertEqual(HTTPStatus.CONFLICT, response.status_code)
