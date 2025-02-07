from .base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = [
    "*",
]

if DEBUG_SILK:
    MIDDLEWARE += [
        "silk.middleware.SilkyMiddleware",
    ]
    INSTALLED_APPS += [
        "silk",
    ]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
