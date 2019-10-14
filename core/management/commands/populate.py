from django.core.management.base import BaseCommand
from core.models import *

class Command(BaseCommand):
    def _create_default_room(self):
        room = Room(name='Default')
        room.save()

    def handle(self, *args, **options):
        self._create_default_room()
