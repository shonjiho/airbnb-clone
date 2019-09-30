from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.shortcuts import render
from . import models
from . import forms


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
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

    model = models.Room
    # auto
    # context : { "room" : room }


def search(request):
    form = forms.SearchForm(request.GET)
    if form.is_valid():
        print(form.cleaned_data)
        city = form.cleaned_data.get("city")
        room_type = form.cleaned_data.get("room_type")
        country = form.cleaned_data.get("country")
        price = form.cleaned_data.get("price")
        guests = form.cleaned_data.get("guests")
        beds = form.cleaned_data.get("beds")
        bedrooms = form.cleaned_data.get("bedrooms")
        baths = form.cleaned_data.get("baths")
        instant_book = form.cleaned_data.get("instant_book")
        superhost = form.cleaned_data.get("superhost")
        amenities = form.cleaned_data.get("amenities")
        facilities = form.cleaned_data.get("facilities")

        filter_kwargs = {}

        filter_kwargs["city__startswith"] = city
        filter_kwargs["country"] = country
        if room_type is not None:
            filter_kwargs["room_type"] = room_type

        if price is not None:
            filter_kwargs["price__lte"] = price

        if guests is not None:
            filter_kwargs["guests__lte"] = guests

        if beds is not None:
            filter_kwargs["beds__lte"] = beds

        if bedrooms is not None:
            filter_kwargs["bedrooms__lte"] = bedrooms

        if baths is not None:
            filter_kwargs["baths__lte"] = baths

        if instant_book is not None:
            filter_kwargs["instant_book"] = instant_book

        if superhost is not None:
            filter_kwargs["host__superhost"] = superhost

        rooms = models.Room.objects.filter(**filter_kwargs)

        if amenities is not None:
            for amenity in amenities:
                rooms = rooms.filter(amenities=amenity)

        if facilities is not None:
            for facility in facilities:
                rooms = rooms.filter(amenities=facility)

        return render(request, "rooms/search.html", {"form": form, "rooms": rooms})
    else:
        form = forms.SearchForm()
        return render(request, "rooms/search.html", {"form": form})

