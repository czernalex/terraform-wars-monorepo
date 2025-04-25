from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import BooleanRadioFilter, RangeDateFilter
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from main.apps.core.admin import BaseModelAdmin
from main.apps.users.models import User


admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, BaseModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    fieldsets = (
        (_("Login credentials"), {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "classes": [
                    "tab",
                ],
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Personal info"),
            {
                "classes": [
                    "tab",
                ],
                "fields": (
                    "first_name",
                    "last_name",
                ),
            },
        ),
        (
            _("Audit info"),
            {
                "classes": [
                    "tab",
                ],
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = (
        "email",
        "is_active",
        "is_admin",
        "is_staff",
        "is_superuser",
        "created_at",
        "updated_at",
    )
    list_filter = (
        ("is_active", BooleanRadioFilter),
        ("is_admin", BooleanRadioFilter),
        ("is_staff", BooleanRadioFilter),
        ("is_superuser", BooleanRadioFilter),
        ("created_at", RangeDateFilter),
        ("updated_at", RangeDateFilter),
    )
    search_fields = (
        "id",
        "email",
    )
    ordering = ("-created_at",)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
