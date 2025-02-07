from typing import override
from uuid import UUID

from auditlog.registry import auditlog
from django.db import models
from django.db.models.fields import PositiveIntegerField
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractBaseModel
from main.apps.tutorials.models.tutorial_group import TutorialGroup


class Tutorial(AbstractBaseModel):
    tutorial_group = models.ForeignKey(TutorialGroup, on_delete=models.CASCADE, related_name="tutorials")
    tutorial_group_id: UUID

    title = models.CharField(_("Title"), max_length=255)
    assignment = models.TextField(_("Assignment"))

    ordering = PositiveIntegerField(_("Ordering"), default=0)

    class Meta:
        verbose_name = _("Tutorial")
        verbose_name_plural = _("Tutorials")

    @override
    def __str__(self) -> str:
        return f"[{self.tutorial_group.title}] {self.title}"


auditlog.register(Tutorial)
