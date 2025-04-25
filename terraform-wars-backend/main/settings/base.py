import os
from pathlib import Path

import sentry_sdk
from decouple import AutoConfig
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration

from main.settings.secrets import Secrets


config = AutoConfig(os.environ.get("DJANGO_CONFIG_ENV_DIR"))

secrets = Secrets(
    SECRET_KEY=config("SECRET_KEY"),
    DB_PASSWORD=config("DB_PASSWORD"),
    EMAIL_HOST_PASSWORD=config("EMAIL_HOST_PASSWORD"),
    SENTRY_DSN=config("SENTRY_DSN", default=None),
)

ENVIRONMENT = config("ENVIRONMENT", default="production")
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
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
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

SESSION_COOKIE_NAME = "__session"
SESSION_COOKIE_DOMAIN = config("SESSION_COOKIE_DOMAIN")
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", cast=bool, default=True)

CSRF_COOKIE_DOMAIN = config("CSRF_COOKIE_DOMAIN")
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", cast=bool, default=True)

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
    environment=ENVIRONMENT,
    send_default_pii=True,
)


# Unfold Admin


def get_admin_environment() -> list[str]:
    match ENVIRONMENT:
        case "production":
            return ["Production", "danger"]
        case "testing":
            return ["Testing", "warning"]
        case "local":
            return ["Local", "primary"]
        case _:
            raise ValueError(f"Invalid environment: {ENVIRONMENT}")


UNFOLD = {
    "SITE_TITLE": "Terraform Wars",
    "SITE_HEADER": "Terraform Wars",
    "SITE_SUBHEADER": "Site administration",
    "SITE_DROPDOWN": [
        {
            "icon": "settings",
            "title": _("Admin"),
            "link": reverse_lazy("admin:index"),
        },
        {
            "icon": "cloud",
            "title": _("App"),
            "link": FRONTEND_BASE_URL,
        },
        {
            "icon": "api",
            "title": _("API Docs"),
            "link": reverse_lazy("terraform-wars-api:openapi-view"),
        },
        {
            "icon": "key",
            "title": _("Allauth API Docs"),
            "link": reverse_lazy("headless:openapi_html"),
        },
    ],
    "SITE_URL": FRONTEND_BASE_URL,
    "SITE_SYMBOL": "apps",
    "SHOW_HISTORY": True,
    "SHOW_BACK_BUTTON": True,
    "ENVIRONMENT": get_admin_environment(),
    "BORDER_RADIUS": "4px",
    "COLORS": {
        "base": {
            "50": "249 250 251",
            "100": "243 244 246",
            "200": "229 231 235",
            "300": "209 213 219",
            "400": "156 163 175",
            "500": "107 114 128",
            "600": "75 85 99",
            "700": "55 65 81",
            "800": "31 41 55",
            "900": "17 24 39",
            "950": "3 7 18",
        },
        "primary": {
            "50": "240 253 250",
            "100": "204 251 241",
            "200": "153 246 228",
            "300": "94 234 212",
            "400": "45 212 191",
            "500": "20 184 166",
            "600": "13 148 136",
            "700": "15 118 110",
            "800": "17 94 89",
            "900": "19 78 74",
            "950": "4 47 46",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",  # text-base-500
            "subtle-dark": "var(--color-base-400)",  # text-base-400
            "default-light": "var(--color-base-600)",  # text-base-600
            "default-dark": "var(--color-base-300)",  # text-base-300
            "important-light": "var(--color-base-900)",  # text-base-900
            "important-dark": "var(--color-base-100)",  # text-base-100
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Audit log"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Log entries"),
                        "icon": "update",
                        "link": reverse_lazy("admin:auditlog_logentry_changelist"),
                        "permission": lambda request: request.user.has_perm("auditlog.view_logentry"),
                    },
                ],
            },
            {
                "title": _("Tutorials"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Tutorial Groups"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:tutorials_tutorialgroup_changelist"),
                        "permission": lambda request: request.user.has_perm("tutorials.view_tutorialgroup"),
                    },
                    {
                        "title": _("Tutorials"),
                        "icon": "description",
                        "link": reverse_lazy("admin:tutorials_tutorial_changelist"),
                        "permission": lambda request: request.user.has_perm("tutorials.view_tutorial"),
                    },
                    {
                        "title": _("Tutorial Submissions"),
                        "icon": "contact_page",
                        "link": reverse_lazy("admin:tutorials_tutorialsubmission_changelist"),
                        "permission": lambda request: request.user.has_perm("tutorials.view_tutorialsubmission"),
                    },
                ],
            },
            {
                "title": _("Users"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "manage_accounts",
                        "link": reverse_lazy("admin:users_user_changelist"),
                        "permission": lambda request: request.user.has_perm("users.view_user"),
                    },
                    {
                        "title": _("Email Addresses"),
                        "icon": "email",
                        "link": reverse_lazy("admin:account_emailaddress_changelist"),
                        "permission": lambda request: request.user.has_perm("accounts.view_emailaddress"),
                    },
                    {
                        "title": _("Auth Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.user.has_perm("auth.view_group"),
                    },
                ],
            },
        ],
    },
}
