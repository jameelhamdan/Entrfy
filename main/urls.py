from django.urls import path, include

app_name = 'main'
urlpatterns = [
    path('', include('main.api.views'))

]
