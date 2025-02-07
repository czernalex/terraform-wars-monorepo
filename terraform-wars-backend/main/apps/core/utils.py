from django.test import Client, TestCase


class ApiClientTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client(HTTP_CONTENT_TYPE="application/json")
