import pytest
from model_bakery import baker

from main.apps.tutorials.models.tutorial import Tutorial
from main.apps.tutorials.models.tutorial_group import TutorialGroup
from main.apps.users.models import User


@pytest.mark.django_db
class TestTutorialGroupQuerySet:
    def test_for_user(self):
        user = baker.make(User)
        tutorial_group = baker.make(TutorialGroup, user=user)

        assert TutorialGroup.objects.for_user(user.id).count() == 1
        assert TutorialGroup.objects.for_user(user.id).first() == tutorial_group

    def test_annotate_tutorial_count(self):
        user = baker.make(User)
        tutorial_group = baker.make(TutorialGroup, user=user)
        baker.make(Tutorial, tutorial_group=tutorial_group)
        baker.make(Tutorial, tutorial_group=tutorial_group)

        assert TutorialGroup.objects.annotate_tutorial_count().first()._tutorial_count == 2

    def test_annotate_tutorial_count_with_no_tutorials(self):
        user = baker.make(User)
        baker.make(TutorialGroup, user=user)

        assert TutorialGroup.objects.annotate_tutorial_count().first()._tutorial_count == 0
