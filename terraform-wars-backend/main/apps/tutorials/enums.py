from django.db import models


class TutorialGroupState(models.TextChoices):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
