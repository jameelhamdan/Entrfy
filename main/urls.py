from django.urls import path, include

app_name = 'main'
urlpatterns = [
    path('followers/', include('main.followers.views')),
    path('interests/', include('main.interests.views')),
    path('matching/', include('main.matching.views')),

]
