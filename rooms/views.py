from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.utils import timezone
from django.shortcuts import render, reverse, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from . import models
from . import forms
from users import mixins as user_mixins


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 12
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


class EditRoomView(user_mixins.LoginInOnlyView, UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoginInOnlyView, DetailView):
    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomSearch(View):
    def get(self, request):
        form = forms.SearchForm(request.GET)
        if form.is_valid():
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

            for amenity in amenities:
                filter_kwargs["amenities"] = amenity
            for facility in facilities:
                filter_kwargs["facilities"] = facility

            qs = models.Room.objects.filter(**filter_kwargs)

            paginator = Paginator(qs, 5, orphans=5)

            page = request.GET.get("page", 1)
            rooms = paginator.get_page(page)

            return render(request, "rooms/search.html", {"form": form, "rooms": rooms})
        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can`t delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))

    return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))


class EditPhotoView(user_mixins.LoginInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.Photo
    template_name = "rooms/edit_photo.html"
    pk_url_kwarg = "photo_pk"
    fields = ("caption",)
    success_message = "Photo Updated"

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoginInOnlyView, FormView):
    model = models.Photo
    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Upload.")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))
