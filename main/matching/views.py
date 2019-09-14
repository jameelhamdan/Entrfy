from rest_framework import generics
from django.urls import path
from auth.backend.decorators import view_authenticate
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
