from rest_framework import views, generics, status, response
from django.urls import path
from main.api.serializers import AddInterestSerializer, AddUserInterestSerializer, ListInterestSerializer
from auth.middleware import view_allow_any, view_authenticate
from extensions.helpers import serializer_to_json
from extensions.mixins import APIViewMixin


@view_authenticate()
class AddNewInterestView(APIViewMixin, generics.CreateAPIView):
    serializer_class = AddInterestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        interest = serializer.validate(request.data)

        result = {
            'interest': interest.name,
        }

        return self.get_response(message='Successfully Added Interest', result=result)


@view_authenticate()
class AddInterestView(APIViewMixin, generics.CreateAPIView):
    serializer_class = AddUserInterestSerializer

    def create(self, request, *args, **kwargs):
        setattr(request.data, 'request', request)
        serializer = self.get_serializer(data=request.data)
        serializer.validate(request.data)

        return self.get_response(message='Successfully Added Interest')


@view_authenticate()
class ListUserInterests(APIViewMixin, generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        user = self.request.current_user
        interests_list = serializer_to_json(ListInterestSerializer, user.interests.all())
        message = 'Successfully Retrieved Interests for user {}'.format(user.user_name)

        return self.get_response(message=message, result=interests_list)


urlpatterns = [
    path('interest/add_new/', AddNewInterestView.as_view(), name='add_new_interest'),
    path('interest/add/', AddInterestView.as_view(), name='add_interest'),

    path('interest/list/all', ListUserInterests.as_view(), name='list_all_interest'),
    path('interest/list/', ListUserInterests.as_view(), name='list_interest'),
]
