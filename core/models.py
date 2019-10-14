import uuid
from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Camera(models.Model):
    name = models.CharField(max_length=200, default='New camera', null=False, blank=False)
    identifier = models.CharField(max_length=200, null=False, blank=False)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, default=1, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

