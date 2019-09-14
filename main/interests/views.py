from rest_framework import generics
from django.urls import path
from main.interests.serializers import AddInterestSerializer, AddUserInterestSerializer, ListInterestSerializer
from auth.backend.decorators import view_authenticate
from extensions.helpers import serializer_to_json
from extensions.mixins import APIViewMixin
from main.models import Interest

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
class ListAllInterests(APIViewMixin, generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        interests_list = serializer_to_json(ListInterestSerializer, Interest.nodes.all())
        message = 'Successfully Retrieved All Interests!'

        return self.get_response(message=message, result=interests_list)


@view_authenticate()
class ListUserInterests(APIViewMixin, generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        user = self.request.current_user
        interests_list = serializer_to_json(ListInterestSerializer, user.interests.all())
        message = 'Successfully Retrieved Interests for user {}'.format(user.user_name)

        return self.get_response(message=message, result=interests_list)


urlpatterns = [
    path('add_new/', AddNewInterestView.as_view(), name='add_new_interest'),
    path('add/', AddInterestView.as_view(), name='add_interest'),

    path('list/all/', ListAllInterests.as_view(), name='list_all_interest'),
    path('list/', ListUserInterests.as_view(), name='list_interest'),
]
