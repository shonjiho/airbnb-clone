from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for f in facilities:
            Facility.objects.create(name=f)
        num = len(facilities)
        self.stdout.write(self.style.SUCCESS(f"{num} facilities make!!"))
