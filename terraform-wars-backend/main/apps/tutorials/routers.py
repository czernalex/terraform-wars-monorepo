from http import HTTPStatus

from ninja import Router
from ninja.pagination import paginate

from main.apps.core.types import AuthedHttpRequest
from main.apps.tutorials.managers import TutorialGroupQuerySet
from main.apps.tutorials.schemas import TutorialGroupListSchema

tutorial_groups_router = Router()


@tutorial_groups_router.get(
    "/",
    url_name="tutorial_groups_list",
    response={HTTPStatus.OK: list[TutorialGroupListSchema]},
    description="Get the tutorial groups",
)
@paginate
def get_tutorial_groups(request: AuthedHttpRequest) -> TutorialGroupQuerySet:
    pass
