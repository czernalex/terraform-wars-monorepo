from http import HTTPStatus

from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from ninja import Router


auth_router = Router()


@auth_router.post(
    "/csrf/",
    url_name="csrf",
    response={HTTPStatus.NO_CONTENT: None},
    auth=None,
    description="Get a CSRF token",
)
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request: HttpRequest) -> HttpResponse:
    return HttpResponse(status=HTTPStatus.NO_CONTENT)
