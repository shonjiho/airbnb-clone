from django.contrib import admin
from . import models


@admin.register(models.Facility)
class Facility(admin.ModelAdmin):
    pass


@admin.register(models.Amenity)
class AmenityTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.HouseRule)
class HouseRuleTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Photo)
class PhoteAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    pass
