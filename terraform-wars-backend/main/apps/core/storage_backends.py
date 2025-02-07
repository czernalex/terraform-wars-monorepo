from django.conf import settings
from django.core.files.storage import FileSystemStorage


class PrivateMediaStorage(FileSystemStorage):
    location = settings.PRIVATE_MEDIA_ROOT
    base_url = settings.PRIVATE_MEDIA_URL
    file_overwrite = False


private_media_storage = PrivateMediaStorage()


# TODO: Add S3 storage
