from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),
    # path('room/login/',views.login,name="login")
    path('create_room/',views.createRoom,name="create_room"),
]
