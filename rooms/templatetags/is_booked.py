from django import template
from reservations import models as reservation_models
import datetime

register = template.Library()


@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return None
    try:
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        reservation_models.BookedDay.objects.get(day=date, reservation__room=room)
        return True
    except reservation_models.BookedDay.DoesNotExist:
        return False
