from http import HTTPStatus

from django.test import TestCase


class HealthCheckTestCase(TestCase):
    def test_healthcheck(self):
        response = self.client.get("/healthcheck/")
        self.assertEqual(HTTPStatus.OK, response.status_code)
