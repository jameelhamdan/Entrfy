from rest_framework import generics
from auth.serializers import LoginSerializer, RegisterSerializer, RefreshTokenSerializer
from auth.backend.jwt import create_auth_token
from auth.backend.decorators import view_allow_any, view_authenticate
from _common.mixins import APIViewMixin


@view_allow_any()
class LoginView(APIViewMixin, generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token = create_auth_token(user.uuid, user.secret_key)

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
class RefreshTokenView(APIViewMixin, generics.CreateAPIView):
    serializer_class = RefreshTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth_token = serializer.validated_data

        result = {
            'new_token': auth_token,
        }
        return self.get_response(message='Successfully Refreshed Token', result=result)
