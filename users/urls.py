from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile-user/<str:pk>/', views.profileUser, name='profile_user'),
    path('update_user/', views.updateUser, name='update_user'),

    path('activate-user/<uidb64>/<token>/', views.activateUser, name='activate_user'),
    path('generate-link/', views.generateLink, name='generate_link'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name="password_reset"),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),

    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
    template_name='password_reset_confirm.html'),
    name="password_reset_confirm"),
    
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),
]   