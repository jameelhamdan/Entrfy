from django.urls import path, include

handler404 = 'extensions.errors.handler404'
handler500 = 'extensions.errors.handler500'

urlpatterns = [
    path('me/', include('main.urls'), name='main'),
    path('auth/', include('auth.urls'), name='auth'),
    path('chat/', include('chat.views'), name='chat'),
]
