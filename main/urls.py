from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.createRoom, name='create_room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update_room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete_room'),
    path('update-message/<str:pk>/', views.updateMessage, name='update_message'),
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete_message'),
    path('all-topics/', views.allTopics, name='all_topics')
]
   