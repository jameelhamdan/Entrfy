from rest_framework import views, generics
from django.urls import path
from main.api.serializers import AddInterestSerializer, AddUserInterestSerializer, ListInterestSerializer
from rest_framework import status
from rest_framework.response import Response
from auth.middleware import view_allow_any, view_authenticate
from extensions.helpers import serializer_to_json


@view_authenticate()
class AddNewInterestView(generics.CreateAPIView):
    serializer_class = AddInterestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        interest = serializer.validate(request.data)

        result_data = {
            'success': True,
            'message': 'Successfully Added Interest',
            'result': {
                'interest': interest.name,
            }
        }

        return Response(result_data, status=status.HTTP_200_OK)


@view_authenticate()
class AddInterestView(generics.CreateAPIView):
    serializer_class = AddUserInterestSerializer

    def create(self, request, *args, **kwargs):
        setattr(request.data, 'request', request)
        serializer = self.get_serializer(data=request.data)
        serializer.validate(request.data)

        result_data = {
            'success': True,
            'message': 'Successfully Added Interest To Me',
            'result': {}
        }

        return Response(result_data, status=status.HTTP_200_OK)


@view_authenticate()
class ListUserInterests(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        user = self.request.current_user
        interests_list = serializer_to_json(ListInterestSerializer, user.interests.all())
        result_data = {
            'success': True,
            'message': 'Successfully Retrieved Interests for user {}'.format(user.user_name),
            'result': interests_list
        }

        return Response(result_data, status=status.HTTP_200_OK)


urlpatterns = [
    path('interest/add_new/', AddNewInterestView.as_view(), name='add_new_interest'),
    path('interest/add/', AddInterestView.as_view(), name='add_interest'),

    path('interest/list/all', ListUserInterests.as_view(), name='list_all_interest'),
    path('interest/list/', ListUserInterests.as_view(), name='list_interest'),
]
