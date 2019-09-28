from django.core.management.base import BaseCommand
from django_seed import Seed
import random
from lists import models as list_models
from users.models import User
from rooms.models import Room


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=3, type=int, help="how to many create lists??"
        )

    def handle(self, *args, **options):
        num = options.get("number")

        seeder = Seed.seeder()
        users = User.objects.all()
        rooms = Room.objects.all()

        seeder.add_entity(
            list_models.List, num, {"user": lambda x: random.choice(users)}
        )
        created = seeder.execute()
        cleaned = created[list_models.List]
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*to_add)

        self.stdout.write(self.style.SUCCESS(f"{num} lists created!!"))
