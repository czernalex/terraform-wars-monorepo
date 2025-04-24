from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateRangeFilter

from main.apps.users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Oprávnění"),
            {
                "classes": (
                    "collapse",
                    "wide",
                ),
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
            _("Uživatelské údaje"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "id",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            _("Přihlašovací údaje"),
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
        (
            _("Oprávnění"),
            {
                "classes": ("wide",),
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
            _("Uživatelské údaje"),
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                ),
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
        "is_active",
        "is_admin",
        "is_staff",
        "is_superuser",
        ("created_at", DateRangeFilter),
        ("updated_at", DateRangeFilter),
    )
    search_fields = (
        "id",
        "email",
    )
    ordering = ("-created_at",)
