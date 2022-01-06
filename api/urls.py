from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),
    path('get-rooms/', views.getRooms),
    path('get-rooms/<int:id>/', views.getRoom),
    path('create-rooms/', views.createRoom),
    path('edit-rooms/<int:id>/', views.editRoom),
    path('get-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('get-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]