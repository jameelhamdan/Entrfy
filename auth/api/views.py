from rest_framework import views, generics, status, response
from django.urls import path
from auth.api.serializers import LoginSerializer, RegisterSerializer
from auth.backend.jwt import create_auth_token
from auth.middleware import view_allow_any, view_authenticate
from extensions.helpers import serializer_to_json
from extensions.mixins import APIViewMixin


@view_allow_any()
class LoginView(APIViewMixin, generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token = create_auth_token(user.uuid)

        if not token:
            raise Exception('Login Failed')
        else:
            result = {
                'uuid': user.uuid,
                'token': token
            }
            return self.get_response(message='Successfully Logged in', result=result)


@view_allow_any()
class RegisterView(APIViewMixin, generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        result = {
            'uuid': user.uuid,
        }
        return self.get_response(message='Successfully Registered User', result=result)


@view_authenticate()
class HelloView(APIViewMixin, views.APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.currenttt_user
        return self.get_response(message='Hello, {}!'.format(user.user_name))


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('auth_test/', HelloView.as_view(), name='auth_test'),
]
