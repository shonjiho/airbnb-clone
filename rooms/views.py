from django.views.generic import ListView
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse
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


def room_detail(request, pk):
    try:
        room = room_models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"pk": pk, "room": room})
    except room_models.Room.DoesNotExist:
        # On DEBUG == False, Http404() show templates/404.html -> this is default
        raise Http404()
