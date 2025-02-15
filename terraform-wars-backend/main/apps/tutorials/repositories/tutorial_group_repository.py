import abc
from typing import Iterable
from uuid import UUID

from django.db import transaction

from main.apps.tutorials.models.tutorial_group import TutorialGroup
from main.apps.tutorials.schemas import (
    CreateTutorialGroupSchema,
    GetTutorialGroupFilterSchema,
    UpdateTutorialGroupSchema,
)
from main.apps.users.models.user import User


class TutorialGroupRepository(abc.ABC):
    @abc.abstractmethod
    def get_all(self, filters: GetTutorialGroupFilterSchema) -> Iterable[TutorialGroup]:
        pass

    @abc.abstractmethod
    def create(self, user: User, data: CreateTutorialGroupSchema) -> TutorialGroup:
        pass

    @abc.abstractmethod
    def get_by_id(self, tutorial_group_id: UUID) -> TutorialGroup:
        pass

    @abc.abstractmethod
    def update(self, user: User, tutorial_group_id: UUID, data: UpdateTutorialGroupSchema) -> TutorialGroup:
        pass

    @abc.abstractmethod
    def delete(self, user: User, tutorial_group_id: UUID) -> None:
        pass


class DjangoORMTutorialGroupRepository(TutorialGroupRepository):
    def get_all(self, filters: GetTutorialGroupFilterSchema) -> Iterable[TutorialGroup]:
        return TutorialGroup.objects.filter(filters.get_filter_expression())

    @transaction.atomic
    def create(self, user: User, data: CreateTutorialGroupSchema) -> TutorialGroup:
        return TutorialGroup.objects.create(user=user, **data)

    def get_by_id(self, tutorial_group_id: UUID) -> TutorialGroup:
        return TutorialGroup.objects.select_related("user").get(id=tutorial_group_id)

    def _get_by_id_for_update(self, user: User, tutorial_group_id: UUID) -> TutorialGroup:
        return (
            TutorialGroup.objects.select_for_update(of=("self",))
            .select_related("user")
            .for_user(user.id)
            .get(id=tutorial_group_id)
        )

    @transaction.atomic
    def update(self, user: User, tutorial_group_id: UUID, data: UpdateTutorialGroupSchema) -> TutorialGroup:
        tutorial_group = self._get_by_id_for_update(user, tutorial_group_id)
        for key, value in data.items():
            setattr(tutorial_group, key, value)
        tutorial_group.save()
        return tutorial_group

    @transaction.atomic
    def delete(self, user: User, tutorial_group_id: UUID) -> None:
        tutorial_group = self._get_by_id_for_update(user, tutorial_group_id)
        tutorial_group.delete()
