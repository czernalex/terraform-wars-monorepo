import os
from pathlib import Path

import sentry_sdk
from decouple import AutoConfig
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration

from main.settings.secrets import Secrets


config = AutoConfig(os.environ.get("DJANGO_CONFIG_ENV_DIR"))

secrets = Secrets(
    SECRET_KEY=config("SECRET_KEY"),
    DB_PASSWORD=config("DB_PASSWORD"),
    EMAIL_HOST_PASSWORD=config("EMAIL_HOST_PASSWORD"),
    SENTRY_DSN=config("SENTRY_DSN"),
)

BASE_DIR = Path(__file__).resolve().parent.parent

BASE_PROTOCOL = config("BASE_PROTOCOL", default="https")
BASE_DOMAIN = config("BASE_DOMAIN")
BASE_URL = f"{BASE_PROTOCOL}://{BASE_DOMAIN}"

FRONTEND_BASE_URL = config("FRONTEND_BASE_URL", default="https://app.terraformwars.com")

DEBUG = config("DEBUG", cast=bool, default=False)
DEBUG_SILK = config("DEBUG_SILK", cast=bool, default=False)

SECRET_KEY = secrets.SECRET_KEY


# Application definition


# Apps

INSTALLED_APPS = [
    "main.apps.api_auth",
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
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": secrets.DB_PASSWORD,
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
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

LANGUAGE_CODE = "en"
TIME_ZONE = "Europe/Prague"
USE_TZ = True

USE_I18N = True
USE_L10N = True
USE_THOUSAND_SEPARATOR = True

LANGUAGES = [
    ("en", _("language.en")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]


# Static files (CSS, JavaScript, Images)

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    BASE_DIR.parent / "static",
]

STATIC_LOCATION = "static"
MEDIA_LOCATION = "media"

USE_CLOUD_STORAGE = config("USE_CLOUD_STORAGE", cast=bool, default=True)

if USE_CLOUD_STORAGE:
    GCS_BUCKET_NAME = config("GCS_BUCKET_NAME")
    common_storage_backend = "storages.backends.gcloud.GoogleCloudStorage"
    common_options = {
        "bucket_name": GCS_BUCKET_NAME,
    }

    STORAGES = {
        "default": {
            "BACKEND": common_storage_backend,
            "OPTIONS": {
                **common_options,
                "location": MEDIA_LOCATION,
                "iam_sign_blob": True,
                "file_overwrite": False,
            },
        },
        "staticfiles": {
            "BACKEND": common_storage_backend,
            "OPTIONS": {
                **common_options,
                "location": STATIC_LOCATION,
                "default_acl": "publicRead",
                "file_overwrite": True,
            },
        },
    }

    GCS_BASE_URL = f"https://storage.googleapis.com/{GCS_BUCKET_NAME}"
    STATIC_URL = f"{GCS_BASE_URL}/{STATIC_LOCATION}/"
    MEDIA_URL = f"{GCS_BASE_URL}/{MEDIA_LOCATION}/"
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.filesystem.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    MEDIA_ROOT = BASE_DIR.parent / MEDIA_LOCATION

    STATIC_URL = f"{BASE_URL}/{STATIC_LOCATION}/"
    MEDIA_URL = f"{BASE_URL}/{MEDIA_LOCATION}/"


## ALLAUTH

ACCOUNT_LOGIN_METHODS = ("email",)
ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "password1*",
]

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False
ACCOUNT_DEFAULT_HTTP_PROTOCOL = BASE_PROTOCOL
ACCOUNT_USER_DISPLAY = lambda user: user.email  # noqa
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_PASSWORD_RESET_BY_CODE_ENABLED = False

### ALLAUTH HEADLESS

HEADLESS_ONLY = True
HEADLESS_CLIENTS = ("browser",)
HEADLESS_SERVE_SPECIFICATION = True
HEADLESS_SPECIFICATION_TEMPLATE_NAME = "headless/spec/swagger_cdn.html"

HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": FRONTEND_BASE_URL + "/auth/verify-email/{key}",
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


# ALLOWED_HOSTS, CSRF and CORS

SESSION_COOKIE_DOMAIN = config("SESSION_COOKIE_DOMAIN")
CSRF_COOKIE_DOMAIN = config("CSRF_COOKIE_DOMAIN")
CSRF_COOKIE_NAME = config("CSRF_COOKIE_NAME")

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=lambda v: [s.strip() for s in v.split(",")])

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

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", cast=lambda v: [s.strip() for s in v.split(",")])
if "0.0.0.0" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("0.0.0.0")

SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", cast=bool, default=True)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Email

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@terraformwars.com")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = secrets.EMAIL_HOST_PASSWORD
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)


# Sentry

sentry_sdk.init(
    dsn=secrets.SENTRY_DSN,
    integrations=[DjangoIntegration()],
    environment=config("SENTRY_ENVIRONMENT"),
    send_default_pii=True,
)
