import uuid
from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_default():
        room, created = Room.objects.get_or_create(name="Default")
        return room

class Camera(models.Model):
    name = models.CharField(max_length=200, default='New camera', null=False, blank=False)
    identifier = models.CharField(max_length=200, null=False, blank=False)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, default=Room.get_default, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
