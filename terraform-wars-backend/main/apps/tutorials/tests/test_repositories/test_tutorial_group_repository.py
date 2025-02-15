import pytest
from model_bakery import baker

from main.apps.tutorials.enums import TutorialGroupState
from main.apps.tutorials.models.tutorial_group import TutorialGroup
from main.apps.tutorials.repositories.tutorial_group_repository import DjangoORMTutorialGroupRepository
from main.apps.tutorials.schemas import GetTutorialGroupFilterSchema
from main.apps.users.models import User


@pytest.mark.django_db
class TestTutorialGroupRepository:
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
