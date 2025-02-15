from .base import *  # noqa


CONSTANCE_BACKEND = "constance.backends.memory.MemoryBackend"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
