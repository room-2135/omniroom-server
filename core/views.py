from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from .models import *
from .serializers import *

def index(request, identifier=Room.get_default().id):
    context = {
        'identifier': int(identifier),
        'rooms': Room.objects.all(),
        'cameras': Camera.objects.filter(room=int(identifier)).all()
    }
    return render(request, "index.html", context)

class RoomsList(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomsRetrieve(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomsCreate(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class RoomsUpdate(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class CamerasList(generics.ListAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class CamerasRetrieve(generics.RetrieveAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
