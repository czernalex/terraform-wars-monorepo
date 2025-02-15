from typing import override
from uuid import UUID

from auditlog.registry import auditlog
from django.db import models
from django.db.models.fields import PositiveIntegerField
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractBaseModel
from main.apps.tutorials.models.tutorial_group import TutorialGroup
from main.apps.tutorials.managers import TutorialQuerySet


class Tutorial(AbstractBaseModel):
    tutorial_group = models.ForeignKey(TutorialGroup, on_delete=models.CASCADE, related_name="tutorials")
    tutorial_group_id: UUID

    title = models.CharField(_("Title"), max_length=255)
    assignment = models.TextField(_("Assignment"))
    assignment_validation = models.TextField(_("Assignment Validation"))

    ordering = PositiveIntegerField(_("Ordering"), default=0)

    objects = TutorialQuerySet.as_manager()

    class Meta:
        verbose_name = _("Tutorial")
        verbose_name_plural = _("Tutorials")

    @override
    def __str__(self) -> str:
        return f"[{self.tutorial_group.title}] - Tutorial: {self.title} ({self.ordering})"


auditlog.register(Tutorial)
