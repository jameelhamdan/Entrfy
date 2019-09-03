from rest_framework import views, generics, status, response
from django.urls import path
from main.interests.serializers import AddInterestSerializer, AddUserInterestSerializer, ListInterestSerializer
from auth.middleware import view_allow_any, view_authenticate
from extensions.helpers import serializer_to_json
from extensions.mixins import APIViewMixin


@view_authenticate()
class AddNewInterestView(APIViewMixin, generics.CreateAPIView):
    serializer_class = AddInterestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        interest = serializer.validated_data

        result = {
            'interest': interest.name,
        }

        return self.get_response(message='Successfully Added Interest', result=result)


@view_authenticate()
class AddInterestView(APIViewMixin, generics.CreateAPIView):
    serializer_class = AddUserInterestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)

        return self.get_response(message='Successfully Added Interest')


@view_authenticate()
class ListUserInterests(APIViewMixin, generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        user = self.request.current_user
        interests_list = serializer_to_json(ListInterestSerializer, user.interests.all())
        message = 'Successfully Retrieved Interests for user {}'.format(user.user_name)

        return self.get_response(message=message, result=interests_list)


urlpatterns = [
    # matches
    path('add_new/', AddNewInterestView.as_view(), name='add_new_interest'),
    path('add/', AddInterestView.as_view(), name='add_interest'),

    path('list/all/', ListUserInterests.as_view(), name='list_all_interest'),
    path('list/', ListUserInterests.as_view(), name='list_interest'),
]
