from typing import TYPE_CHECKING, Self
from uuid import UUID

from django.db import models
from django.db.models import Count

if TYPE_CHECKING:
    from main.apps.tutorials.models import TutorialGroup, Tutorial, TutorialSubmission, TutorialGroupConfig


class TutorialGroupQuerySet(models.QuerySet["TutorialGroup"]):
    def for_user(self, user_id: UUID) -> Self:
        return self.filter(user_id=user_id)

    def annotate_tutorial_count(self) -> Self:
        return self.annotate(_tutorial_count=Count("tutorials", distinct=True))


class TutorialQuerySet(models.QuerySet["Tutorial"]):
    def for_tutorial_group(self, tutorial_group_id: UUID) -> Self:
        return self.filter(tutorial_group_id=tutorial_group_id)


class TutorialSubmissionQuerySet(models.QuerySet["TutorialSubmission"]):
    def for_tutorial(self, tutorial_id: UUID) -> Self:
        return self.filter(tutorial_id=tutorial_id)

    def for_user(self, user_id: UUID) -> Self:
        return self.filter(user_id=user_id)


class TutorialGroupConfigQuerySet(models.QuerySet["TutorialGroupConfig"]):
    def for_user(self, user_id: UUID) -> Self:
        return self.filter(user_id=user_id)
