from django.core.management.base import BaseCommand
from rooms.models import RoomType


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        types = ["Private Room", "Public Room", "Special Room", "Another Room"]
        for type in types:
            RoomType.objects.create(name=type)
        num = len(types)
        self.stdout.write(self.style.SUCCESS(f"{num} Room Type MAKE!!"))
