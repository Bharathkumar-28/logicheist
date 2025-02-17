from typing import Any
from django.core.management.base import BaseCommand
from adminpanel.models import speechquiz2

class Command(BaseCommand):
    help = "This command inserts category data into the speechquiz model"

    def handle(self, *args: Any, **options: Any):
        # Deleting existing data
        speechquiz2.objects.all().delete()

        titles = ["easy", 'hard']
        names = ['animals', 'birds']
        images = ["https://picsum.photos/id/1/200/300", "https://picsum.photos/id/2/200/300"]
        data_list = [
            ["lion", 'cat', 'rat', 'dog', 'tree'],
            ["sparrow", 'eagle', 'parrot', 'crow', 'pigeon']
        ]

        # Creating new records
        for title, name, image, data in zip(titles, names, images, data_list):
            speechquiz2.objects.create(title=title, name=name, image=image, data=data)

        self.stdout.write(self.style.SUCCESS("Completed inserting data"))
