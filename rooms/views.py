from django.shortcuts import render
from django.core.paginator import Paginator
from . import models


def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)  # Paginator(<item_list>, page_size)
    rooms = paginator.get_page(page)
    # rooms = paginator.page(page)
    return render(request, "rooms/home.html", {"page": rooms})
