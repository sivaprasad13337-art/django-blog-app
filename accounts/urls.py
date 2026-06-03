from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.fun),
    path('register/', views.createUser, name='Register-User'),
    path('login/', views.userLogin, name='Login-User'),
    path('setProfile/', views.setProfile, name='Set-Profile'),
    path('logout/', views.userLogout, name='Logout-User'),
    path('getProfile/<str:user_name>', views.getProfile, name='Get-Profile'),
    
    path(
        'reset_password/',auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'),name='Password-Reset'),
    path(
        'reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),name='password_reset_confirm'),
    path(
        'reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]