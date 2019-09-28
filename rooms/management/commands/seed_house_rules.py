from django.core.management.base import BaseCommand
from rooms.models import HouseRule


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        rules = ["don`t smoke", "don`t pet", "don`t party", "don`t event"]
        for r in rules:
            HouseRule.objects.create(name=r)
        num = len(rules)
        self.stdout.write(self.style.SUCCESS(f"{num} Amenities MAKE!!"))
