from datetime import datetime
from unittest.mock import patch

import pytest
from django.test import RequestFactory

from main import VERSION
from main.apps.core.context_processors import current_year, terraform_wars_api_version


@pytest.fixture
def request_factory():
    return RequestFactory()


@patch("django.utils.timezone.now")
def test_current_year(mock_timezone_now, request_factory):
    mock_timezone_now.return_value = datetime(2022, 1, 1)
    context = current_year(request_factory.get("/"))
    assert "current_year" in context
    assert 2022 == context["current_year"]


def test_terraform_api_version(request_factory):
    context = terraform_wars_api_version(request_factory.get("/"))
    assert "terraform_wars_api_version" in context
    assert VERSION == context["terraform_wars_api_version"]
