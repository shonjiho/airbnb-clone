from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "room_count")

    def room_count(self, obj):
        return obj.rooms.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Phot Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src={obj.file.url}/>')

    get_thumbnail.short_description = "Thumnail"


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    inlines = [PhotoInline]

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More About the Space",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    filter_horizontal = ("amenities", "facilities")

    raw_id_fields = ("amenities",)

    ordering = ("name", "price", "bedrooms")

    list_display = (
        "name",
        "city",
        "country",
        "instant_book",
        "host",
        "price",
        "bedrooms",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = ("city", "host__superhost", "country")

    search_fields = ("=city", "^host__username")

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    # count_amenities.short_description = "Super Sexy"
