from rest_framework import generics
from django.urls import path
from main.followers.serializers import ListUsersSerializer, FollowUserSerializer
from auth.backend.decorators import view_authenticate
from extensions.helpers import serializer_to_json
from extensions.mixins import APIViewMixin


@view_authenticate()
class FollowUserView(APIViewMixin, generics.CreateAPIView):
    serializer_class = FollowUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        result = serializer.validated_data

        return self.get_response(message='Successfully Followed User', result={'followed': result.user_name, 'me': self.request.current_user.user_name})


@view_authenticate()
class ListUserFollowedView(APIViewMixin, generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        user = self.request.current_user
        interests_list = serializer_to_json(ListUsersSerializer, user.get_followed)
        message = 'Successfully Retrieved Followed users for {}'.format(user.user_name)

        return self.get_response(message=message, result=interests_list)


urlpatterns = [
    path('user/', FollowUserView.as_view(), name='follow_user'),
    path('all/', ListUserFollowedView.as_view(), name='all_people_followed'),

]
