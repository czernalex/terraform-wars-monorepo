from typing import override
from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractBaseModel


class TutorialGroup(AbstractBaseModel):
    title = models.CharField(_("Title"), max_length=255)

    class Meta:
        verbose_name = _("Tutorial Group")
        verbose_name_plural = _("Tutorial Groups")

    @override
    def __str__(self) -> str:
        return self.title

    @property
    def tutorial_count(self) -> int:
        if hasattr(self, "_tutorial_count"):
            return self._tutorial_count

        return self.tutorials.count()


auditlog.register(TutorialGroup)
