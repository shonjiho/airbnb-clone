from django.views.generic import ListView, DetailView
from django.utils import timezone
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
