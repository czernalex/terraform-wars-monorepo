from datetime import datetime

import pytest
from django.test import RequestFactory

from main.apps.core.context_processors import current_year, terraform_wars_api_version


@pytest.fixture
def request_factory():
    return RequestFactory()


def test_current_year(mocker, request_factory: RequestFactory):
    mock_timezone_now = mocker.patch(
        "main.apps.core.context_processors.timezone.now", return_value=datetime(2022, 1, 1)
    )
    context = current_year(request_factory.get("/"))
    assert "current_year" in context
    assert 2022 == context["current_year"]
    mock_timezone_now.assert_called_once()


def test_terraform_api_version(mocker, request_factory: RequestFactory):
    mocker.patch("main.apps.core.context_processors.VERSION", "1.0.0")
    context = terraform_wars_api_version(request_factory.get("/"))
    assert "terraform_wars_api_version" in context
    assert "1.0.0" == context["terraform_wars_api_version"]
