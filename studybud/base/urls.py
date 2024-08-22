from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.LoginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('room_page/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userprofile, name="user-profile"),
    path('create_room/', views.createRoom, name="create_room"),
    path('update_room/<str:pk>/', views.updateRoom, name="update_room"),
    path('delete_room/<str:pk>/', views.deleteRoom, name="delete_room"),
    path('delete_message/<str:pk>/', views.delete_message, name="delete_message"),
    path('update-user/', views.updateUser, name="update-user"),
]

