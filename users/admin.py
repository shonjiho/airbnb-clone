from django.contrib import admin
from . import models

# admin model


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):

    pass
