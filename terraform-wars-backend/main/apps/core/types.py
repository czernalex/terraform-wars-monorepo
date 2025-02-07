from django.http import HttpRequest

from main.apps.users.models import User


class AuthedHttpRequest(HttpRequest):
    user: User
