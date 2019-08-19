from django.urls import path, include


urlpatterns = [
    path('', include('main.urls'), name='main'),
    path('auth/', include('auth.urls'), name='auth'),
]