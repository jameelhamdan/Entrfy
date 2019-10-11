from django.urls import path
from auth import views

app_name = 'auth'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('reset_password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('refresh/', views.RefreshTokenView.as_view(), name='refresh'),
]
