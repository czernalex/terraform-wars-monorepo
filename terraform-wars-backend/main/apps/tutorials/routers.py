from http import HTTPStatus
from typing import Iterable

from anydi import auto
from ninja import Router
from ninja.pagination import paginate

from main.apps.core.types import AuthedHttpRequest
from main.apps.tutorials.models.tutorial_group import TutorialGroup
from main.apps.tutorials.schemas import TutorialGroupListSchema
from main.apps.tutorials.services.tutorial_group_service import TutorialGroupService

tutorial_groups_router = Router()


@tutorial_groups_router.get(
    "/",
    url_name="tutorial-group-list",
    response={HTTPStatus.OK: list[TutorialGroupListSchema]},
    description="Get the tutorial groups",
)
@paginate
def get_tutorial_groups(
    request: AuthedHttpRequest, tutorial_group_service: TutorialGroupService = auto
) -> Iterable[TutorialGroup]:
    return tutorial_group_service.get_tutorial_groups()
