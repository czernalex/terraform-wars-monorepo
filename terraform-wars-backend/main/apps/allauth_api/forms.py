from django import forms
from django.http import HttpRequest

from main.apps.users.models import User


class UserSignupForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def signup(self, request: HttpRequest, user: User) -> User:
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user
