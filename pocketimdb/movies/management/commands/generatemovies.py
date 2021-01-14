from django.core.management.base import BaseCommand
from ...factories import MovieFactory

class Command(BaseCommand):
    help = 'Generates specified number of movies'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int)

    def handle(self, *args, **options):
        count = options['count']

        if not count or count < 1:
            count = 1

        for _ in range(count):
            MovieFactory()

        messageEnd = 'movies' if count > 1 else 'movie'
        self.stdout.write(self.style.SUCCESS('Successfully created %d %s.' % (count, messageEnd)))