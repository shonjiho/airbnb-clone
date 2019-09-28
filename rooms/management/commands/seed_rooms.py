from django.core.management.base import BaseCommand, CommandError
from django_seed import Seed
import random
from rooms import models as rooms_model
from users import models as users_model


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How to many room make?"
        )

    def handle(self, *args, **options):
        num = options.get("number")

        seeder = Seed.seeder()
        all_users = users_model.User.objects.all()
        room_types = rooms_model.RoomType.objects.all()

        seeder.add_entity(
            rooms_model.Room,
            num,
            {
                "name": seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "guests": lambda x: random.randint(1, 20),
                "price": lambda x: random.randint(1, 300),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        amenities = rooms_model.Amenity.objects.all()
        facilities = rooms_model.Facility.objects.all()
        rules = rooms_model.HouseRule.objects.all()

        inserted_pks = seeder.execute()
        for pk in inserted_pks[rooms_model.Room]:
            room = rooms_model.Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 30)):
                rooms_model.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/photos_seed/{random.randint(1, 31)}.webp",
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)

            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)

            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{num} Rooms Created"))
