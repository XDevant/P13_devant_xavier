"""
This is to make sure Django wakes up with Postgres back end.
Also load data dumped previously.
"""
from psycopg2 import OperationalError as PsycopgOperationalError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """Django command to move from sqlite to Postgres."""
    help = 'Django command to move from sqlite to Postgres.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        call_command('wait_for_db')
        call_command('collectstatic', '--noinput')
        call_command('makemigrations')
        call_command('migrate', '--run-syncdb')
        call_command('loaddata', 'db.json')