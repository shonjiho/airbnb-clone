from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.shortcuts import render
from django_countries import countries
from . import models as room_models


class HomeView(ListView):

    """ HomeView Definition """

    model = room_models.Room
    paginate_by = 10
    ordering = "created"
    paginate_orphans = 5
    context_object_name = "rooms"  # default object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = room_models.Room
    # auto
    # context : { "room" : room }


def search(request):
    city = request.GET.get("city", "AnyWhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    beds = int(request.GET.get("beds", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    baths = int(request.GET.get("bedrooms", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    room_types = room_models.RoomType.objects.all()
    amenities = room_models.Amenity.objects.all()
    facilities = room_models.Facility.objects.all()

    form = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "price": price,
        "guests": guests,
        "beds": beds,
        "bedrooms": bedrooms,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = dict()

    if city != "AnyWhere":
        filter_args["city__startswith"] = city
    filter_args["country"] = country
    if room_type != 0:
        filter_args["room_type__pk"] = room_type
    if price != 0:
        filter_args["price__lte"] = price
    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms
    if beds != 0:
        filter_args["beds__gte"] = beds
    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant == True:
        filter_args["instant_book"] = True
    if superhost == True:
        filter_args["host__superhost"] = True

    # if len(amenities) > 0:
    #     for s_amenity in s_amenities:
    #         filter_args["amenities__pk"] = int(s_amenity)

    # if len(facilities) > 0:
    #     for s_facility in s_facilities:
    #         filter_args["facilities__pk"] = int(s_facility)

    rooms = room_models.Room.objects.filter(**filter_args)

    for s_facility in s_facilities:
        rooms = rooms.filter(facilities__pk=s_facility)
    for s_amenity in s_amenities:
        rooms = rooms.filter(facilities__pk=s_amenity)

    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})

