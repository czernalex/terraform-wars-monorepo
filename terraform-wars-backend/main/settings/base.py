import os
from pathlib import Path

import sentry_sdk
from decouple import AutoConfig
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

config = AutoConfig(os.environ.get("DJANGO_CONFIG_ENV_DIR"))

BASE_DIR = Path(__file__).resolve().parent.parent

BASE_PROTOCOL = config("BASE_PROTOCOL", default="https")
BASE_DOMAIN = config("BASE_DOMAIN", default="")
BASE_URL = f"{BASE_PROTOCOL}://{BASE_DOMAIN}"

FRONTEND_BASE_URL = config("FRONTEND_BASE_URL", default="http://127.0.0.1:4242")

DEBUG = False
DEBUG_SILK = config("DEBUG_SILK", cast=bool, default=False)

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", cast=lambda v: [s.strip() for s in v.split(",")])
if "0.0.0.0" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("0.0.0.0")


# Application definition


# Apps

INSTALLED_APPS = [
    "main.apps.allauth_api",
    "main.apps.core",
    "main.apps.tutorials",
    "main.apps.users",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "allauth",
    "allauth.account",
    "allauth.headless",
    "allauth.socialaccount",
    "anydi.ext.django",
    "auditlog",
    "corsheaders",
    "django_extensions",
    "rangefilter",
]


# Middleware

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "main.urls"


# Templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "main.apps.core.context_processors.current_year",
                "main.apps.core.context_processors.terraform_wars_api_version",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                )
            ],
            "builtins": [],
        },
    },
]


# WSGI application

WSGI_APPLICATION = "main.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="prosinka"),
        "USER": config("DB_USER", default="prosinka"),
        "PASSWORD": config("DB_PASSWORD", default="prosinka"),
        "HOST": config("DB_HOST", default="127.0.0.1"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

ATOMIC_REQUESTS = False
AUTOCOMMIT = True

# Password validation

AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Internationalization

LANGUAGE_CODE = "cs"
TIME_ZONE = "Europe/Prague"
USE_TZ = True

USE_I18N = True
USE_L10N = True
USE_THOUSAND_SEPARATOR = True

LANGUAGES = [
    ("cs", _("language.cs")),
    ("en", _("language.en")),
]


# Static files (CSS, JavaScript, Images)


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    BASE_DIR.parent / "static",
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.filesystem.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
    "private": {
        "BACKEND": "main.apps.core.storage_backends.PrivateMediaStorage",
    },
}

STATIC_LOCATION = "static"
STATIC_URL = f"{BASE_URL}/{STATIC_LOCATION}/"

PUBLIC_MEDIA_LOCATION = "media"
MEDIA_ROOT = BASE_DIR.parent / "media"
MEDIA_URL = f"{BASE_URL}/{PUBLIC_MEDIA_LOCATION}/"

PRIVATE_MEDIA_LOCATION = "private-media"
PRIVATE_MEDIA_ROOT = BASE_DIR.parent / "private-media"
PRIVATE_MEDIA_URL = f"{BASE_URL}/{PRIVATE_MEDIA_LOCATION}/"


## ALLAUTH

HEADLESS_ONLY = True

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_DEFAULT_HTTP_PROTOCOL = BASE_PROTOCOL
ACCOUNT_USER_DISPLAY = lambda user: user.email  # noqa
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGOUT_ON_GET = True

ACCOUNT_SIGNUP_FORM_CLASS = "main.apps.allauth_api.forms.UserSignupForm"

HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": FRONTEND_BASE_URL + "/auth/verify-email?key={key}",
    "account_reset_password": FRONTEND_BASE_URL + "/auth/password-reset",
    "account_reset_password_from_key": FRONTEND_BASE_URL + "/auth/password-reset/{key}",
    "account_signup": FRONTEND_BASE_URL + "/auth/sign-up",
}


# AnyDI - dependency injection

ANYDI = {
    "PATCH_NINJA": True,
    "MODULES": [
        "main.apps.tutorials.module.TutorialsModule",
    ],
}


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

AUDITLOG_INCLUDE_ALL_MODELS = False


# CSRF and CORS

CSRF_TRUSTED_ORIGINS = config("CSRF_ALLOWED_ORIGINS", cast=lambda v: [s.strip() for s in v.split(",")])

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "cache-control",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "sentry-trace",
)

CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=lambda v: [s.strip() for s in v.split(",")])


# Email

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="admin@terraform-wars.cz")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = config("EMAIL_HOST", default="smtp.sendgrid.net")
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="apikey")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="apikey")
EMAIL_PORT = config("EMAIL_PORT", default=587)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)


# Sentry

sentry_sdk.init(
    dsn=config("SENTRY_DSN", default=""),
    integrations=[DjangoIntegration(), CeleryIntegration()],
    environment=config("ENVIRONMENT", default="production"),
    send_default_pii=True,
)


# Celery

CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="redis://redis:6379/0")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="redis://redis:6379/0")

CELERY_TIMEZONE = "UTC"
CELERY_TASK_SERIALIZER = "pickle"
CELERY_IGNORE_RESULT = True
CELERYD_CONCURRENCY = 1

CELERYBEAT_SCHEDULE = {}
