from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# admin model


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "superhost",
                    "birthdate",
                    "language",
                    "currency",
                    "login_method"
                )
            },
        ),
    )

    list_display = (
        "username",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
        "superhost",
        "email_verified",
        "email_secret",
        "login_method"
    )
    list_filter = UserAdmin.list_filter + ("superhost",)
