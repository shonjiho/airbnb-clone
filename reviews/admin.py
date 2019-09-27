from django.contrib import admin
from reviews import models

# Register your models here.


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("__str__", "rating_average")
