from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AccountChangeForm, AccountCreationForm
from .models import Account


class AccountAdmin(UserAdmin):
    model: type = Account
    add_form: type = AccountCreationForm
    form: type = AccountChangeForm
    list_display: list = [
        "username",
        "email",
        "first_name",
        "last_name",
        "account_type",
    ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("email", "first_name", "last_name")}),
        ("Account Info", {"fields": ("account_type", "rating")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )


admin.site.register(Account, AccountAdmin)
