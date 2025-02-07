from django.http import HttpRequest
from django.utils import timezone

from main import VERSION


def current_year(request: HttpRequest) -> dict[str, int]:
    return {
        "current_year": timezone.now().year,
    }


def terraform_wars_api_version(request: HttpRequest) -> dict[str, str]:
    return {
        "terraform_wars_api_version": VERSION,
    }
