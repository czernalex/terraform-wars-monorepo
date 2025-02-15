from typing import override
from uuid import UUID

from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractBaseModel
from main.apps.users.models import User
from main.apps.tutorials.models import TutorialGroup
from main.apps.tutorials.managers import TutorialGroupConfigQuerySet


class TutorialGroupConfig(AbstractBaseModel):
    tutorial_group = models.ForeignKey(TutorialGroup, on_delete=models.CASCADE, related_name="configs")
    tutorial_group_id: UUID
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tutorial_group_configs")
    user_id: UUID

    config = models.JSONField(_("Config"), blank=True, null=True)

    objects = TutorialGroupConfigQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tutorial_group", "user"],
                name="unique_user_tutorial_group_config",
            ),
        ]
        verbose_name = _("Tutorial Group Config")
        verbose_name_plural = _("Tutorial Group Configs")

    @override
    def __str__(self) -> str:
        return f"[{self.tutorial_group.title}] - {self.user.email} Config"


auditlog.register(TutorialGroupConfig)
