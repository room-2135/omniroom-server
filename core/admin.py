from django.contrib import admin
from .models import *

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    pass
