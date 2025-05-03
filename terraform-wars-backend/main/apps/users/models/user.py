from typing import override

from auditlog.registry import auditlog
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractBaseModel
from main.apps.users.managers import UserManager, UserQuerySet


class User(AbstractBaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email"), unique=True, max_length=128)

    first_name = models.CharField(_("First name"), max_length=255, blank=True, null=True)
    last_name = models.CharField(_("Last name"), max_length=255, blank=True, null=True)

    is_active = models.BooleanField(
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    is_admin = models.BooleanField(default=False, help_text=_("Designates whether the user can access the admin site."))
    is_staff = models.BooleanField(
        default=False, help_text=_("Designates whether the user can log into this admin site.")
    )

    objects = UserManager.from_queryset(UserQuerySet)()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @override
    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        if self.last_name and self.first_name:
            return f"{self.first_name} {self.last_name}"

        return self.email


auditlog.register(User)
