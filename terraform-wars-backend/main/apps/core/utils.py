from django.test import Client, TestCase


class ApiClientTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client(HTTP_CONTENT_TYPE="application/json")
