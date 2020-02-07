from django.urls import path
from . import views as room_views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", room_views.RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit", room_views.EditRoomView.as_view(), name="edit"),
    path("search/", room_views.RoomSearch.as_view(), name="search"),
]
