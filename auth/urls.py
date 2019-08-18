from django.urls import path, include

app_name = 'auth'
urlpatterns = [
    path('', include('auth.api.views'))
]
