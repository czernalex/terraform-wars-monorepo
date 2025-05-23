from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import include, path

from main.api import root_api_router


def trigger_error(_: HttpRequest) -> HttpResponse:
    division_by_zero = 1 / 0  # noqa: F841
    return HttpResponse(status=200)


urlpatterns = [
    path("healthcheck/", lambda request: HttpResponse(status=200)),
    path("accounts/", include("allauth.urls")),
    path("_allauth/", include("allauth.headless.urls")),
    path("api/", root_api_router.urls),
    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += [
        path("sentry-debug/", trigger_error),
        path("400/", lambda request: render(request, "400.html"), name="400"),
        path("403/", lambda request: render(request, "403.html"), name="403"),
        path("404/", lambda request: render(request, "404.html"), name="404"),
        path("500/", lambda request: render(request, "500.html"), name="500"),
    ]
    urlpatterns += staticfiles_urlpatterns(prefix="/static/")
    urlpatterns += static(settings.MEDIA_LOCATION, document_root=settings.MEDIA_ROOT)


if settings.DEBUG and settings.DEBUG_SILK:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
