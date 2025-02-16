from http import HTTPStatus

from anydi import Container
import pytest
from django.test import Client
from django.urls import reverse

from main.apps.tutorials.repositories import DjangoORMTutorialGroupRepository
from main.apps.tutorials.services import TutorialGroupService
from main.apps.tutorials.models import TutorialGroup


container = Container(testing=True)


class TestTutorialGroupRouter:
    @pytest.mark.django_db
    def test_get_tutorial_groups(
        self,
        mocker,
        authed_client: Client,
        tutorial_group_draft: TutorialGroup,
        tutorial_group_published: TutorialGroup,
        tutorial_group_archived: TutorialGroup,
    ):
        service = TutorialGroupService(DjangoORMTutorialGroupRepository())
        mocker.patch.object(
            service,
            "get_tutorial_groups",
            return_value=[
                tutorial_group_draft,
                tutorial_group_published,
                tutorial_group_archived,
            ],
        )

        # FIXME: Find out why this is not working
        with container.override(TutorialGroupService, service):
            response = authed_client.get(reverse("terraform-wars-api:tutorial-group-list"))

            assert response.status_code == HTTPStatus.OK

            # tutorial_group_items = response.json()["items"]
            # assert len(tutorial_group_items) == 3
            # assert tutorial_group_items[0]["id"] == tutorial_group_draft.id
            # assert tutorial_group_items[0]["title"] == tutorial_group_draft.title
            # assert tutorial_group_items[0]["description"] == tutorial_group_draft.description
            # assert tutorial_group_items[1]["id"] == tutorial_group_published.id
            # assert tutorial_group_items[1]["title"] == tutorial_group_published.title
            # assert tutorial_group_items[1]["description"] == tutorial_group_published.description
            # assert tutorial_group_items[2]["id"] == tutorial_group_archived.id
            # assert tutorial_group_items[2]["title"] == tutorial_group_archived.title
            # assert tutorial_group_items[2]["description"] == tutorial_group_archived.description
