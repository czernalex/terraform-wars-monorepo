import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(models.Model):
    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.id)
