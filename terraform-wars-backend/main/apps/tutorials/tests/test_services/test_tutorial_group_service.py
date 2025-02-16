import pytest
import uuid

from main.apps.tutorials.repositories import DjangoORMTutorialGroupRepository
from main.apps.tutorials.schemas import (
    GetTutorialGroupFilterSchema,
    CreateTutorialGroupSchema,
    UpdateTutorialGroupSchema,
)
from main.apps.tutorials.services import TutorialGroupService
from main.apps.tutorials.models import TutorialGroup
from main.apps.tutorials.enums import TutorialGroupState
from main.apps.core.exceptions import ForbiddenError, NotFoundError


class TestTutorialGroupService:
    def test_get_tutorial_groups(self, mocker, tutorial_group_draft, tutorial_group_published):
        repository = DjangoORMTutorialGroupRepository()
        mocker.patch.object(
            repository,
            "get_all",
            return_value=[
                tutorial_group_draft,
                tutorial_group_published,
            ],
        )

        service = TutorialGroupService(repository)
        filters = GetTutorialGroupFilterSchema()

        result = service.get_tutorial_groups(filters)

        assert len(result) == 2
        assert result[0].id == tutorial_group_draft.id
        assert result[0].title == "Tutorial Group 1"
        assert result[0].state == TutorialGroupState.DRAFT
        assert result[0].description == "Description 1"
        assert result[1].id == tutorial_group_published.id
        assert result[1].title == "Tutorial Group 2"
        assert result[1].state == TutorialGroupState.PUBLISHED
        assert result[1].description == "Description 2"

        repository.get_all.assert_called_once_with(filters)

    def test_get_tutorial_groups_filter_by_state(self, mocker, tutorial_group_published):
        repository = DjangoORMTutorialGroupRepository()
        mocker.patch.object(
            repository,
            "get_all",
            return_value=[
                tutorial_group_published,
            ],
        )

        service = TutorialGroupService(repository)
        filters = GetTutorialGroupFilterSchema(state=TutorialGroupState.PUBLISHED)

        result = service.get_tutorial_groups(filters)

        assert len(result) == 1
        assert result[0].id == tutorial_group_published.id
        assert result[0].title == "Tutorial Group 2"
        assert result[0].state == TutorialGroupState.PUBLISHED
        assert result[0].description == "Description 2"

        repository.get_all.assert_called_once_with(filters)

    def test_create_tutorial_group(self, mocker, user, tutorial_group_draft):
        repository = DjangoORMTutorialGroupRepository()
        mocker.patch.object(
            repository,
            "create",
            return_value=tutorial_group_draft,
        )

        service = TutorialGroupService(repository)
        data = CreateTutorialGroupSchema(title="Tutorial Group 1", description="Description 1")

        result = service.create_tutorial_group(user, data)

        assert result.id == tutorial_group_draft.id
        assert result.title == "Tutorial Group 1"
        assert result.description == "Description 1"
        assert result.state == TutorialGroupState.DRAFT

        repository.create.assert_called_once_with(user, data)

    def test_get_tutorial_group(self, mocker, tutorial_group_draft):
        repository = DjangoORMTutorialGroupRepository()
        mocker.patch.object(
            repository,
            "get_by_id",
            return_value=tutorial_group_draft,
        )

        service = TutorialGroupService(repository)
        result = service.get_tutorial_group(tutorial_group_draft.id)

        assert result.id == tutorial_group_draft.id
        assert result.title == "Tutorial Group 1"
        assert result.description == "Description 1"
        assert result.state == TutorialGroupState.DRAFT

        repository.get_by_id.assert_called_once_with(tutorial_group_draft.id)

    def test_get_tutorial_group_not_found(self, mocker):
        repository = DjangoORMTutorialGroupRepository()
        mocker.patch.object(repository, "get_by_id", side_effect=NotFoundError("Tutorial group not found"))

        service = TutorialGroupService(repository)
        with pytest.raises(NotFoundError):
            service.get_tutorial_group(uuid.uuid4())

    @pytest.mark.django_db
    def test_update_tutorial_group(self, mocker, user, tutorial_group_draft):
        repository = DjangoORMTutorialGroupRepository()
        mocker.patch.object(
            repository,
            "get_by_id_for_update",
            return_value=tutorial_group_draft,
        )
        mocker.patch.object(
            repository,
            "update",
            return_value=TutorialGroup(
                id=tutorial_group_draft.id,
                title="Tutorial Group 1",
                description="Updated description",
                state=TutorialGroupState.PUBLISHED,
            ),
        )

        service = TutorialGroupService(repository)
        result = service.update_tutorial_group(
            user,
            tutorial_group_draft.id,
            UpdateTutorialGroupSchema(
                title="Tutorial Group 1", description="Updated description", state=TutorialGroupState.PUBLISHED
            ),
        )

        assert result.id == tutorial_group_draft.id
        assert result.title == "Tutorial Group 1"
        assert result.description == "Updated description"
        assert result.state == TutorialGroupState.PUBLISHED

        repository.get_by_id_for_update.assert_called_once_with(user, tutorial_group_draft.id)
        repository.update.assert_called_once_with(
            tutorial_group_draft,
            UpdateTutorialGroupSchema(
                title="Tutorial Group 1", description="Updated description", state=TutorialGroupState.PUBLISHED
            ),
        )

    @pytest.mark.django_db
    def test_update_tutorial_group_not_found(self, mocker, user):
        repository = DjangoORMTutorialGroupRepository()
        mocker.patch.object(repository, "get_by_id_for_update", side_effect=NotFoundError("Tutorial group not found"))

        service = TutorialGroupService(repository)
        with pytest.raises(NotFoundError):
            service.update_tutorial_group(
                user,
                uuid.uuid4(),
                UpdateTutorialGroupSchema(
                    title="Tutorial Group 1", description="Updated description", state=TutorialGroupState.DRAFT
                ),
            )

    @pytest.mark.django_db
    def test_update_tutorial_group_archived(self, mocker, user, tutorial_group_archived):
        repository = DjangoORMTutorialGroupRepository()
        mocker.patch.object(repository, "get_by_id_for_update", return_value=tutorial_group_archived)

        service = TutorialGroupService(repository)
        with pytest.raises(ForbiddenError):
            service.update_tutorial_group(
                user,
                tutorial_group_archived.id,
                UpdateTutorialGroupSchema(
                    title="Tutorial Group 1",
                    description="Updated description",
                    state=TutorialGroupState.DRAFT,
                ),
            )

    @pytest.mark.django_db
    def test_delete_tutorial_group(self, mocker, user, tutorial_group_draft):
        repository = DjangoORMTutorialGroupRepository()
        mocker.patch.object(
            repository,
            "get_by_id_for_update",
            return_value=tutorial_group_draft,
        )
        mocker.patch.object(repository, "delete", return_value=None)

        service = TutorialGroupService(repository)
        service.delete_tutorial_group(user, tutorial_group_draft.id)

        repository.get_by_id_for_update.assert_called_once_with(user, tutorial_group_draft.id)
        repository.delete.assert_called_once_with(tutorial_group_draft)

    @pytest.mark.django_db
    def test_delete_tutorial_group_not_found(self, mocker, user):
        repository = DjangoORMTutorialGroupRepository()
        mocker.patch.object(repository, "get_by_id_for_update", side_effect=NotFoundError("Tutorial group not found"))

        service = TutorialGroupService(repository)
        with pytest.raises(NotFoundError):
            service.delete_tutorial_group(user, uuid.uuid4())
