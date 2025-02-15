from typing import override
from uuid import UUID

from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractBaseModel
from main.apps.tutorials.enums import TutorialGroupState
from main.apps.tutorials.managers import TutorialGroupQuerySet
from main.apps.users.models.user import User


class TutorialGroup(AbstractBaseModel):
    user = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.SET_NULL, null=True, blank=True)
    user_id: UUID

    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    state = models.CharField(
        _("State"), max_length=255, choices=TutorialGroupState.choices, default=TutorialGroupState.DRAFT
    )

    objects = TutorialGroupQuerySet.as_manager()

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
