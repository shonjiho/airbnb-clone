from django.core.management.base import BaseCommand
from django_seed import Seed
import random
from django.utils.timezone import datetime, timedelta
from reservations import models as reservation_models
from users.models import User
from rooms.models import Room

NAME = "reservations"


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=3, type=int, help="how to many create reservations??"
        )

    def handle(self, *args, **options):
        num = options.get("number")

        seeder = Seed.seeder()
        users = User.objects.all()
        rooms = Room.objects.all()

        seeder.add_entity(
            reservation_models.Reservation,
            num,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25)),
            },
        )

        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{num} reservations created!!"))
