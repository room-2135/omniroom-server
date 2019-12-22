# core/serializers.py
from rest_framework import serializers
from .models import *

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'created_at', 'updated_at']
        model = Room

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'identifier', 'room', 'created_at', 'updated_at']
        model = Camera
