from datetime import datetime
from unittest.mock import patch

from django.test import TestCase, RequestFactory
from django.utils import timezone

from main import VERSION
from main.apps.core.context_processors import current_year, terraform_wars_api_version


class ContextProcauessorsTestCase(TestCase):
    def setUp(self) -> None:
        self.request_factory = RequestFactory()

    def test_current_year(self):
        context = current_year(self.request_factory.get("/"))
        self.assertIn("current_year", context)
        self.assertEqual(timezone.now().year, context["current_year"])

    @patch("django.utils.timezone.now")
    def test_current_year_mocked(self, mock_timezone_now):
        mock_timezone_now.return_value = datetime(2022, 1, 1)
        context = current_year(self.request_factory.get("/"))
        self.assertIn("current_year", context)
        self.assertEqual(2022, context["current_year"])

    def test_terraform_api_version(self):
        context = terraform_wars_api_version(self.request_factory.get("/"))
        self.assertIn("terraform_wars_api_version", context)
        self.assertEqual(VERSION, context["terraform_wars_api_version"])
