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
    room_types = room_models.RoomType.objects.all()

    form = {"city": city, "s_country": country, "s_room_type": room_type}

    choices = {"countries": countries, "room_types": room_types}

    return render(request, "rooms/search.html", {**form, **choices})

