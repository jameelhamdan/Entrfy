from rest_framework import views, generics
from django.urls import path
from auth.api.serializers import LoginSerializer, RegisterSerializer
from auth.models import User
from rest_framework import status
from rest_framework.response import Response
from auth.jwt import create_auth_token


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        request_data = self.request.data

        serializer = self.get_serializer(data=request.data)
        user = serializer.validate(self.request.data)

        token = create_auth_token(user.uuid)

        result_data = {
            'success': False,
            'message': 'Log in Error',
            'data': None
        }

        if token:
            result_data = {
                'success': True,
                'message': 'Successfully Logged in',
                'data': {
                    'uuid': request_data.get('uuid'),
                    'token': token
                }
            }

        return Response(result_data, status=status.HTTP_201_CREATED)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        request_data = self.request.data

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.create_user(
            user_name=request_data.get('user_name'),
            email=request_data.get('email'),
            password=request_data.get('password')
        )

        result_data = {
            'success': True,
            'message': 'Successfully Registered User',
            'data': {
                'uuid': user.uuid
            }
        }

        return Response(result_data, status=status.HTTP_201_CREATED)


urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
]
