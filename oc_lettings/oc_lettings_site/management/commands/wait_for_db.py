"""
Django command to wait for the database to be available.
We want to make sure Docker compose does not start migrations
before db is ready.
"""
import time
from django.core.management import call_command
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
        db_up = 0
        time.sleep(1)
        while db_up < 30:
            try:
                call_command("check", "--database default")
                db_up = 30
            except (PsycopgOperationalError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                db_up += 1
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
