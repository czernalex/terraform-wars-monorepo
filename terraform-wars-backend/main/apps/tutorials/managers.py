from typing import Self
from uuid import UUID

from django.db import models
from django.db.models import Count


class TutorialGroupQuerySet(models.QuerySet):
    def annotate_tutorial_count(self) -> Self:
        return self.annotate(_tutorial_count=Count("tutorials", distinct=True))


class TutorialQuerySet(models.QuerySet):
    def for_tutorial_group(self, tutorial_group_id: UUID) -> Self:
        return self.filter(tutorial_group_id=tutorial_group_id)


class TutorialSubmissionQuerySet(models.QuerySet):
    def for_tutorial(self, tutorial_id: UUID) -> Self:
        return self.filter(tutorial_id=tutorial_id)

    def for_user(self, user_id: UUID) -> Self:
        return self.filter(user_id=user_id)


class TutorialGroupConfigQuerySet(models.QuerySet):
    def for_user(self, user_id: UUID) -> Self:
        return self.filter(user_id=user_id)
