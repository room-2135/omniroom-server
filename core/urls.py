from django.urls import path

from . import views

urlpatterns = [
    path('<identifier>', views.index, name='index'),
    path('rooms', views.RoomsList.as_view()),
    path('rooms', views.RoomsCreate.as_view()),
    path('rooms/<pk>', views.RoomsRetrieve.as_view()),
    path('rooms/<pk>', views.RoomsUpdate.as_view()),
    path('cameras', views.CamerasList.as_view()),
    path('cameras/<pk>', views.CamerasRetrieve.as_view()),
]
