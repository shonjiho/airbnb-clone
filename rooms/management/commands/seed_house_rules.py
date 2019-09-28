from django.core.management.base import BaseCommand
from rooms.models import HouseRule


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--num", help="How many times do you want me to tell you that i love me"
        )

    def handle(self, *args, **options):
        rules = ["don`t smoke", "don`t pet", "don`t party", "don`t event"]
        for r in rules:
            HouseRule.objects.create(name=r)
        num = len(rules)
        self.stdout.write(self.style.SUCCESS(f"{num} Amenities MAKE!!"))
