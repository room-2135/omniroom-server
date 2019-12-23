from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<identifier>', views.index, name='room'),
    path('rooms', views.RoomsList.as_view()),
    path('rooms', views.RoomsCreate.as_view()),
    path('rooms/<pk>', views.RoomsRetrieve.as_view()),
    path('rooms/<pk>', views.RoomsUpdate.as_view()),
    path('cameras', views.CamerasList.as_view()),
    path('cameras/<pk>', views.CamerasRetrieve.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
