from http import HTTPStatus

from ninja import Router

from main.apps.core.types import AuthedHttpRequest
from main.apps.users.models import User
from main.apps.users.schemas import UserDetailSchema

users_router = Router()

@users_router.get(
    "/me/",
    url_name="user_detail",
    response={HTTPStatus.OK: UserDetailSchema},
    description="Get the current user",
)
def get_me(request: AuthedHttpRequest) -> User:
    return request.user
