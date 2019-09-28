from django.core.management.base import BaseCommand
from django_seed import Seed
import random
from reviews import models as reviews_model
from users.models import User
from rooms.models import Room


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=3, type=int, help="how to many create reviews??"
        )

    def handle(self, *args, **options):
        num = options.get("number")

        seeder = Seed.seeder()
        users = User.objects.all()
        rooms = Room.objects.all()

        seeder.add_entity(
            reviews_model.Review,
            num,
            {
                "accuracy": lambda x: random.randint(0, 6),
                "communication": lambda x: random.randint(0, 6),
                "cleanliness": lambda x: random.randint(0, 6),
                "location": lambda x: random.randint(0, 6),
                "check_in": lambda x: random.randint(0, 6),
                "value": lambda x: random.randint(0, 6),
                "user": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{num} reviews created!!"))
