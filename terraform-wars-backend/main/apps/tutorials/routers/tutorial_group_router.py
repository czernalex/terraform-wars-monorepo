from http import HTTPStatus
from typing import Iterable, List
from uuid import UUID

from anydi import auto
from ninja import Body, Query, Router
from ninja.pagination import paginate

from main.apps.core.schemas import ForbiddenErrorSchema, NotFoundErrorSchema
from main.apps.core.types import AuthedHttpRequest
from main.apps.tutorials.models.tutorial_group import TutorialGroup
from main.apps.tutorials.schemas import (
    CreateTutorialGroupSchema,
    GetTutorialGroupFilterSchema,
    TutorialGroupDetailSchema,
    TutorialGroupListSchema,
    UpdateTutorialGroupSchema,
)
from main.apps.tutorials.services.tutorial_group_service import TutorialGroupService

tutorial_groups_router = Router()


@tutorial_groups_router.get(
    "/",
    url_name="tutorial-group-list",
    response={HTTPStatus.OK: List[TutorialGroupListSchema]},
    description="Get the tutorial groups.",
)
@paginate
def get_tutorial_groups(
    request: AuthedHttpRequest,
    filters: GetTutorialGroupFilterSchema = Query(...),
    tutorial_group_service: TutorialGroupService = auto,
) -> Iterable[TutorialGroup]:
    return tutorial_group_service.get_tutorial_groups(filters=filters)


@tutorial_groups_router.post(
    "/",
    url_name="tutorial-group-list",
    response={HTTPStatus.CREATED: TutorialGroupDetailSchema},
    description="Create a new tutorial group.",
)
def create_tutorial_group(
    request: AuthedHttpRequest,
    data: CreateTutorialGroupSchema = Body(...),
    tutorial_group_service: TutorialGroupService = auto,
) -> TutorialGroup:
    user = request.user
    return tutorial_group_service.create_tutorial_group(user, data)


@tutorial_groups_router.get(
    "/{tutorial_group_id}/",
    url_name="tutorial-group-detail",
    response={
        HTTPStatus.OK: TutorialGroupDetailSchema,
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Get the tutorial group by its ID.",
)
def get_tutorial_group(
    request: AuthedHttpRequest, tutorial_group_id: UUID, tutorial_group_service: TutorialGroupService = auto
) -> TutorialGroup:
    return tutorial_group_service.get_tutorial_group(tutorial_group_id)


@tutorial_groups_router.put(
    "/{tutorial_group_id}/",
    url_name="tutorial-group-detail",
    response={
        HTTPStatus.OK: TutorialGroupDetailSchema,
        HTTPStatus.FORBIDDEN: ForbiddenErrorSchema,
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Update the tutorial group.",
)
def update_tutorial_group(
    request: AuthedHttpRequest,
    tutorial_group_id: UUID,
    data: UpdateTutorialGroupSchema = Body(...),
    tutorial_group_service: TutorialGroupService = auto,
) -> TutorialGroup:
    user = request.user
    return tutorial_group_service.update_tutorial_group(user, tutorial_group_id, data)


@tutorial_groups_router.delete(
    "/{tutorial_group_id}/",
    url_name="tutorial-group-detail",
    response={
        HTTPStatus.NO_CONTENT: None,
        HTTPStatus.NOT_FOUND: NotFoundErrorSchema,
    },
    description="Delete the tutorial group.",
)
def delete_tutorial_group(
    request: AuthedHttpRequest, tutorial_group_id: UUID, tutorial_group_service: TutorialGroupService = auto
) -> None:
    user = request.user
    tutorial_group_service.delete_tutorial_group(user, tutorial_group_id)
