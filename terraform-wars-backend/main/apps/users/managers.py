from typing import Any, Optional, Self

from django.contrib.auth.models import BaseUserManager, User
from django.db import models
from django.db.models import Q


class UserManager(BaseUserManager["User"]):
    def create_user(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> User:
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user: User = self.model(email=email, is_active=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)

        return self.create_user(email, password, **extra_fields)


class UserQuerySet(models.QuerySet["User"]):
    def is_active(self, is_active: bool = True) -> Self:
        return self.filter(is_active=is_active)

    def for_email(self, email: str) -> Self:
        return self.filter(email=email)

    def has_permission(self, permission_codename: str) -> Self:
        return self.filter(
            Q(groups__permissions__codename=permission_codename)
            | Q(user_permissions__codename=permission_codename)
            | Q(is_superuser=True)
        )

    def search(self, search_query: str) -> Self:
        qs = self.all()

        for search_term in search_query.split(" "):
            qs = qs.filter(
                Q(first_name__unaccent__icontains=search_term)
                | Q(last_name__unaccent__icontains=search_term)
                | Q(email__icontains=search_term)
            )

        return qs
