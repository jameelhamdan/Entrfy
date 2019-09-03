from rest_framework import views, generics, status, response
from django.urls import path
from main.matching.serializers import *
from auth.middleware import view_allow_any, view_authenticate
from extensions.helpers import serializer_to_json
from extensions.mixins import APIViewMixin


@view_authenticate()
class ListUserMatchesView(APIViewMixin, generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        user = self.request.current_user
        message = 'Successfully Most Similar Matches for {}'.format(user.user_name)

        return self.get_response(message=message, result=user.get_matches())


urlpatterns = [
    path('latest', ListUserMatchesView.as_view(), name='list_matches'),

]
