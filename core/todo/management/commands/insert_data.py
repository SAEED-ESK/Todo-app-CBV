from django.core.management.base import  BaseCommand
from django.contrib.auth.models import User
from faker import Faker

from ...models import Todo

from random import choice

class Command(BaseCommand):
    help = 'Insert some data'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create(username=self.fake.user_name(), password='Test1234#')

        for _ in range(5):
            task = Todo.objects.create(
                user = user,
                title = self.fake.paragraph(nb_sentences=1),
                complete = choice([True, False])
            )