"""
Django command to wait for the database to be available.
We want to make sure Docker compose does not start migrations
before db is ready.
"""
import time

from psycopg2 import OperationalError as PsycopgOperationalError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""
    help = 'Django command to wait for database during containerization.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        time.sleep(5)
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsycopgOperationalError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
