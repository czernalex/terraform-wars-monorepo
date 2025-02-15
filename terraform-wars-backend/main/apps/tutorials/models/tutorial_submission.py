from typing import override
from uuid import UUID

from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.apps.core.models import AbstractBaseModel
from main.apps.tutorials.managers import TutorialSubmissionQuerySet
from main.apps.tutorials.models.tutorial import Tutorial
from main.apps.users.models import User


class TutorialSubmission(AbstractBaseModel):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    tutorial_id: UUID
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id: UUID

    solution = models.TextField(_("Solution"))
    errors = models.JSONField(_("Errors"), blank=True, null=True)

    objects = TutorialSubmissionQuerySet.as_manager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["tutorial", "user"], name="unique_user_tutorial_submission")]
        verbose_name = _("Tutorial Submission")
        verbose_name_plural = _("Tutorial Submissions")

    @override
    def __str__(self) -> str:
        return f"[{self.tutorial.title}] - {self.user.email} Submission"


auditlog.register(TutorialSubmission)
