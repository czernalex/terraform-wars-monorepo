from django.contrib import admin

from main.apps.tutorials.models import TutorialGroup, TutorialUserSubmission, Tutorial


@admin.register(TutorialGroup)
class TutorialGroupAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = (
        "id",
        "title",
    )
    ordering = ("-created_at",)


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ("title", "tutorial_group", "ordering", "created_at")
    list_select_related = ("tutorial_group",)
    search_fields = (
        "id",
        "title",
        "tutorial_group__id",
        "tutorial_group__title",
    )
    ordering = ("ordering", "-created_at")


@admin.register(TutorialUserSubmission)
class TutorialUserSubmissionAdmin(admin.ModelAdmin):
    list_display = ("tutorial", "user", "created_at")
    list_select_related = ("tutorial", "tutorial__tutorial_group", "user")
    search_fields = ("id", "tutorial__id", "tutorial__title", "user__id", "user__email")
    ordering = ("-created_at",)
