import logging
from typing import Iterable
from uuid import UUID

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from main.apps.core.exceptions import ForbiddenError
from main.apps.tutorials.enums import TutorialGroupState
from main.apps.tutorials.models import TutorialGroup
from main.apps.tutorials.repositories import TutorialGroupRepository
from main.apps.tutorials.schemas import (
    CreateTutorialGroupSchema,
    GetTutorialGroupFilterSchema,
    UpdateTutorialGroupSchema,
)
from main.apps.users.models.user import User


logger = logging.getLogger(__name__)


class TutorialGroupService:
    def __init__(self, tutorial_group_repository: TutorialGroupRepository):
        self.tutorial_group_repository = tutorial_group_repository

    def get_tutorial_groups(self, filters: GetTutorialGroupFilterSchema) -> Iterable[TutorialGroup]:
        return self.tutorial_group_repository.get_all(filters)

    def create_tutorial_group(self, user: User, data: CreateTutorialGroupSchema) -> TutorialGroup:
        return self.tutorial_group_repository.create(user, data)

    def get_tutorial_group(self, tutorial_group_id: UUID) -> TutorialGroup:
        return self.tutorial_group_repository.get_by_id(tutorial_group_id)

    @transaction.atomic
    def update_tutorial_group(
        self, user: User, tutorial_group_id: UUID, data: UpdateTutorialGroupSchema
    ) -> TutorialGroup:
        tutorial_group = self.tutorial_group_repository.get_by_id_for_update(user, tutorial_group_id)

        if tutorial_group.state == TutorialGroupState.ARCHIVED:
            logger.warning(f"Tutorial group {tutorial_group.id} is archived and cannot be updated.")
            raise ForbiddenError(
                _("Tutorial group %(tutorial_group_title)s is archived and cannot be updated.")
                % {"tutorial_group_title": tutorial_group.title}
            )

        return self.tutorial_group_repository.update(tutorial_group, data)

    @transaction.atomic
    def delete_tutorial_group(self, user: User, tutorial_group_id: UUID) -> None:
        tutorial_group = self.tutorial_group_repository.get_by_id_for_update(user, tutorial_group_id)
        self.tutorial_group_repository.delete(tutorial_group)
