from django.test import Client
import pytest
import uuid

from main.apps.users.models.user import User
from main.apps.tutorials.models import TutorialGroup
from main.apps.tutorials.enums import TutorialGroupState


@pytest.fixture(scope="session")
def user():
    return User(
        id=uuid.uuid4(),
        email="test@test.com",
        is_active=True,
    )


@pytest.fixture(scope="session")
def tutorial_group_draft(user):
    return TutorialGroup(
        id=uuid.uuid4(),
        user=user,
        title="Tutorial Group 1",
        description="Description 1",
        state=TutorialGroupState.DRAFT,
    )


@pytest.fixture(scope="session")
def tutorial_group_published(user):
    return TutorialGroup(
        id=uuid.uuid4(),
        user=user,
        title="Tutorial Group 2",
        description="Description 2",
        state=TutorialGroupState.PUBLISHED,
    )


@pytest.fixture(scope="session")
def tutorial_group_archived(user):
    return TutorialGroup(
        id=uuid.uuid4(),
        user=user,
        title="Tutorial Group 3",
        description="Description 3",
        state=TutorialGroupState.ARCHIVED,
    )


@pytest.fixture(scope="function")
def authed_client(user):
    client = Client(HTTP_CONTENT_TYPE="application/json")
    client.force_login(user)
    return client
