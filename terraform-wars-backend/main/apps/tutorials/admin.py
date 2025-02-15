from django.contrib import admin

from main.apps.tutorials.models import TutorialGroup, Tutorial, TutorialSubmission
from main.apps.tutorials.models.tutorial_group_config import TutorialGroupConfig


@admin.register(TutorialGroup)
class TutorialGroupAdmin(admin.ModelAdmin):
    list_display = ("title", "state", "created_at", "updated_at")
    search_fields = (
        "id",
        "title",
    )
    list_filter = ("state",)
    ordering = ("-created_at",)


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
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
class TutorialSubmissionAdmin(admin.ModelAdmin):
    list_display = ("tutorial", "user", "created_at", "updated_at")
    list_select_related = ("tutorial", "tutorial__tutorial_group", "user")
    search_fields = ("id", "tutorial__id", "tutorial__title", "user__id", "user__email")
    ordering = ("-created_at",)


@admin.register(TutorialGroupConfig)
class TutorialGroupConfigAdmin(admin.ModelAdmin):
    list_display = ("tutorial_group", "user", "created_at", "updated_at")
    list_select_related = ("tutorial_group", "user")
    search_fields = ("id", "tutorial_group__id", "tutorial_group__title", "user__id", "user__email")
    ordering = ("-created_at",)
