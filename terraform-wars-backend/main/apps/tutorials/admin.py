from django.contrib import admin
from unfold.contrib.filters.admin import RangeDateFilter

from main.apps.core.admin import BaseModelAdmin
from main.apps.tutorials.models import TutorialGroup, Tutorial, TutorialSubmission
from main.apps.tutorials.models.tutorial_group_config import TutorialGroupConfig


@admin.register(TutorialGroup)
class TutorialGroupAdmin(BaseModelAdmin):
    list_display = ("title", "state", "user", "created_at", "updated_at")
    list_select_related = ("user",)
    search_fields = (
        "id",
        "title",
    )
    list_filter = (
        "state",
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
    )
    autocomplete_fields = ("user",)
    ordering = ("-created_at",)


@admin.register(Tutorial)
class TutorialAdmin(BaseModelAdmin):
    list_display = ("title", "tutorial_group", "ordering", "created_at", "updated_at")
    list_select_related = ("tutorial_group",)
    search_fields = (
        "id",
        "title",
        "tutorial_group__id",
        "tutorial_group__title",
    )
    ordering = ("ordering", "-created_at")


@admin.register(TutorialSubmission)
class TutorialSubmissionAdmin(BaseModelAdmin):
    list_display = ("tutorial", "user", "created_at", "updated_at")
    list_select_related = ("tutorial", "tutorial__tutorial_group", "user")
    search_fields = ("id", "tutorial__id", "tutorial__title", "user__id", "user__email")
    ordering = ("-created_at",)


@admin.register(TutorialGroupConfig)
class TutorialGroupConfigAdmin(BaseModelAdmin):
    list_display = ("tutorial_group", "user", "created_at", "updated_at")
    list_select_related = ("tutorial_group", "user")
    search_fields = ("id", "tutorial_group__id", "tutorial_group__title", "user__id", "user__email")
    ordering = ("-created_at",)
