import abc
import logging
from typing import Iterable
from uuid import UUID

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.models.tutorial_group import TutorialGroup
from main.apps.tutorials.schemas import (
    CreateTutorialGroupSchema,
    GetTutorialGroupFilterSchema,
    UpdateTutorialGroupSchema,
)
from main.apps.users.models.user import User


logger = logging.getLogger(__name__)


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
    def get_by_id_for_update(self, user: User, tutorial_group_id: UUID) -> TutorialGroup:
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
        logger.info(f"Creating tutorial group for user {user.id}.")
        tutorial_group = TutorialGroup.objects.create(user=user, **data.model_dump())
        logger.info(f"Tutorial group {tutorial_group.id} created.")
        return tutorial_group

    def get_by_id(self, tutorial_group_id: UUID) -> TutorialGroup:
        try:
            return TutorialGroup.objects.select_related("user").get(id=tutorial_group_id)
        except TutorialGroup.DoesNotExist:
            logger.warning(f"Tutorial group with id {tutorial_group_id} does not exist.")
            raise NotFoundError(
                _("Tutorial group with id %(tutorial_group_id)s does not exist.")
                % {"tutorial_group_id": tutorial_group_id}
            )

    def get_by_id_for_update(self, user: User, tutorial_group_id: UUID) -> TutorialGroup:
        try:
            return (
                TutorialGroup.objects.select_for_update(of=("self",))
                .select_related("user")
                .for_user(user.id)
                .get(id=tutorial_group_id)
            )
        except TutorialGroup.DoesNotExist:
            logger.warning(f"Tutorial group with id {tutorial_group_id} does not exist.")
            raise NotFoundError(
                _("Tutorial group with id %(tutorial_group_id)s does not exist.")
                % {"tutorial_group_id": tutorial_group_id}
            )

    @transaction.atomic
    def update(self, tutorial_group: TutorialGroup, data: UpdateTutorialGroupSchema) -> TutorialGroup:
        logger.info(f"Updating tutorial group {tutorial_group.id}.")
        for key, value in data.model_dump().items():
            setattr(tutorial_group, key, value)
        tutorial_group.save()
        logger.info(f"Tutorial group {tutorial_group.id} updated.")
        return tutorial_group

    @transaction.atomic
    def delete(self, tutorial_group: TutorialGroup) -> None:
        logger.info(f"Deleting tutorial group {tutorial_group.id}.")
        tutorial_group.delete()
        logger.info(f"Tutorial group {tutorial_group.id} deleted.")
