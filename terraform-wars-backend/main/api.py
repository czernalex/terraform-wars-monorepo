from http import HTTPStatus

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.security import SessionAuth
from ninja.throttling import AnonRateThrottle, AuthRateThrottle

from main.apps.core.exceptions import ForbiddenError, NotFoundError, ValidationError
from main.apps.core.schemas import ForbiddenErrorSchema, NotFoundErrorSchema, ValidationErrorSchema
from main.apps.tutorials.routers import tutorial_groups_router
from main.apps.users.routers import users_router


root_api_router = NinjaAPI(
    title="Terraform Wars API",
    urls_namespace="terraform-wars-api",
    version="0.0.1",
    description=(
        "REST API for Terraform Wars frontend."
        "<br>"
        "<br>"
        "Authentication is managed by Django Allauth. Open API specification is available "
        "<a href='https://docs.allauth.org/en/latest/headless/openapi-specification/' target='_blank'>here</a>."
        "<br>"
        "Please note, that the Allauth API endpoints are prefixed with <i>/allauth-api/</i> instead of <i>/_allauth/</i>."
        "<br>"
        "<br>"
        "<a href='/admin' class='btn'>Administration</a>"
    ),
    docs_decorator=staff_member_required if not settings.DEBUG else None,
    servers=[
        {"url": "http://127.0.0.1:8000", "description": "Local development server"},
    ],
    auth=SessionAuth(),
    throttle=[
        AnonRateThrottle(rate="10/s"),
        AuthRateThrottle(rate="100/s"),
    ],
    openapi_extra={
        "info": {
            "contact": {
                "email": "alexczerny1@gmail.com",
            }
        }
    },
)


# Attach exception handlers


@root_api_router.exception_handler(ForbiddenError)
def handle_forbidden_error(request: HttpRequest, exc: ForbiddenError) -> HttpResponse:
    return root_api_router.create_response(
        request,
        data=ForbiddenErrorSchema(detail=str(exc)),
        status=HTTPStatus.FORBIDDEN,
    )


@root_api_router.exception_handler(NotFoundError)
def handle_not_found_error(request: HttpRequest, exc: NotFoundError) -> HttpResponse:
    return root_api_router.create_response(
        request,
        data=NotFoundErrorSchema(detail=str(exc)),
        status=HTTPStatus.NOT_FOUND,
    )


@root_api_router.exception_handler(ValidationError)
def handle_validation_error(request: HttpRequest, exc: ValidationError) -> HttpResponse:
    return root_api_router.create_response(
        request,
        data=ValidationErrorSchema(detail=exc.errors),
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
    )


root_api_router.add_router("/tutorial-groups", tutorial_groups_router, tags=["tutorial-groups"])
root_api_router.add_router("/users", users_router, tags=["users"])
