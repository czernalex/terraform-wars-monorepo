import uuid

import pytest
from model_bakery import baker

from main.apps.core.exceptions import NotFoundError
from main.apps.tutorials.enums import TutorialGroupState
from main.apps.tutorials.models.tutorial_group import TutorialGroup
from main.apps.tutorials.repositories.tutorial_group_repository import DjangoORMTutorialGroupRepository
from main.apps.tutorials.schemas import (
    CreateTutorialGroupSchema,
    GetTutorialGroupFilterSchema,
    UpdateTutorialGroupSchema,
)
from main.apps.users.models import User


@pytest.mark.django_db
class TestDjangoORMTutorialGroupRepository:
    def test_get_all(self):
        user = baker.make(User)
        baker.make(TutorialGroup, user=user, _quantity=2, _bulk_create=True)

        repository = DjangoORMTutorialGroupRepository()
        filters = GetTutorialGroupFilterSchema()

        tutorial_groups = repository.get_all(filters)

        assert len(tutorial_groups) == 2

    def test_get_all_filter_by_user_id(self):
        user = baker.make(User)
        baker.make(TutorialGroup, user=user)
        baker.make(TutorialGroup)

        repository = DjangoORMTutorialGroupRepository()
        filters = GetTutorialGroupFilterSchema(user_id=user.id)

        tutorial_groups = repository.get_all(filters)

        assert len(tutorial_groups) == 1
        assert tutorial_groups[0].user == user

    def test_get_all_filter_by_user_id_without_tutorial_groups(self):
        user = baker.make(User)
        baker.make(TutorialGroup)

        repository = DjangoORMTutorialGroupRepository()
        filters = GetTutorialGroupFilterSchema(user_id=user.id)

        tutorial_groups = repository.get_all(filters)

        assert len(tutorial_groups) == 0

    def test_get_all_filter_by_state(self):
        baker.make(TutorialGroup, state=TutorialGroupState.DRAFT)
        baker.make(TutorialGroup, state=TutorialGroupState.PUBLISHED)

        repository = DjangoORMTutorialGroupRepository()
        filters = GetTutorialGroupFilterSchema(state=TutorialGroupState.PUBLISHED)

        tutorial_groups = repository.get_all(filters)

        assert len(tutorial_groups) == 1
        assert tutorial_groups[0].state == TutorialGroupState.PUBLISHED

    def test_create(self):
        user = baker.make(User)
        data = CreateTutorialGroupSchema(title="Test Tutorial Group", description="Test Description")

        repository = DjangoORMTutorialGroupRepository()
        tutorial_group = repository.create(user, data)

        assert tutorial_group.id is not None
        assert tutorial_group.user == user
        assert tutorial_group.title == "Test Tutorial Group"
        assert tutorial_group.description == "Test Description"
        assert tutorial_group.state == TutorialGroupState.DRAFT

    def test_get_by_id(self):
        tutorial_group = baker.make(TutorialGroup)

        repository = DjangoORMTutorialGroupRepository()
        retrieved_tutorial_group = repository.get_by_id(tutorial_group.id)

        assert retrieved_tutorial_group.id == tutorial_group.id
        assert retrieved_tutorial_group.user == tutorial_group.user
        assert retrieved_tutorial_group.title == tutorial_group.title
        assert retrieved_tutorial_group.description == tutorial_group.description
        assert retrieved_tutorial_group.state == tutorial_group.state

    def test_get_by_id_not_found(self):
        repository = DjangoORMTutorialGroupRepository()

        with pytest.raises(NotFoundError):
            repository.get_by_id(uuid.uuid4())

    def test_get_by_id_for_update(self):
        user = baker.make(User)
        tutorial_group = baker.make(TutorialGroup, user=user)

        repository = DjangoORMTutorialGroupRepository()
        retrieved_tutorial_group = repository.get_by_id_for_update(user, tutorial_group.id)

        assert retrieved_tutorial_group.id == tutorial_group.id
        assert retrieved_tutorial_group.user == user
        assert retrieved_tutorial_group.title == tutorial_group.title
        assert retrieved_tutorial_group.description == tutorial_group.description
        assert retrieved_tutorial_group.state == tutorial_group.state

    def test_get_by_id_for_update_not_found(self):
        user = baker.make(User)
        repository = DjangoORMTutorialGroupRepository()

        with pytest.raises(NotFoundError):
            repository.get_by_id_for_update(user, uuid.uuid4())

    def test_get_by_id_for_update_does_not_belong_to_user(self):
        user = baker.make(User)
        other_user = baker.make(User)
        tutorial_group = baker.make(TutorialGroup, user=other_user)

        repository = DjangoORMTutorialGroupRepository()

        with pytest.raises(NotFoundError):
            repository.get_by_id_for_update(user, tutorial_group.id)

    def test_update(self):
        user = baker.make(User)
        tutorial_group = baker.make(TutorialGroup, user=user)

        repository = DjangoORMTutorialGroupRepository()
        updated_tutorial_group = repository.update(
            tutorial_group,
            UpdateTutorialGroupSchema(
                title="New Title", description="New Description", state=TutorialGroupState.PUBLISHED
            ),
        )

        assert updated_tutorial_group.user == user
        assert updated_tutorial_group.title == "New Title"
        assert updated_tutorial_group.description == "New Description"
        assert updated_tutorial_group.state == TutorialGroupState.PUBLISHED

    def test_delete(self):
        user = baker.make(User)
        tutorial_group = baker.make(TutorialGroup, user=user)

        repository = DjangoORMTutorialGroupRepository()
        repository.delete(tutorial_group)

        with pytest.raises(NotFoundError):
            repository.get_by_id(tutorial_group.id)
