import logging
from typing import Iterable
from uuid import UUID

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

    def update_tutorial_group(
        self, user: User, tutorial_group_id: UUID, data: UpdateTutorialGroupSchema
    ) -> TutorialGroup:
        return self.tutorial_group_repository.update(user, tutorial_group_id, data)

    def delete_tutorial_group(self, user: User, tutorial_group_id: UUID) -> None:
        self.tutorial_group_repository.delete(user, tutorial_group_id)
