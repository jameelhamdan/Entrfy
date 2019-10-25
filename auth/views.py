from rest_framework import generics
from auth.serializers import LoginSerializer, RegisterSerializer, ResetPasswordSerializer, RenewAuthTokenSerializer, RenewRefreshTokenSerializer
from auth.backend.decorators import view_allow_any, view_authenticate, view_authenticate_refresh
from _common.mixins import APIViewMixin


@view_allow_any()
class LoginView(APIViewMixin, generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, auth_token, refresh_token = serializer.validated_data

        result = {
            'uuid': user.uuid,
            'auth_token': auth_token,
            'refresh_token': refresh_token,
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
class ResetPasswordView(APIViewMixin, generics.CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user, auth_token, refresh_token = serializer.validated_data

        result = {
            'uuid': user.uuid,
            'auth_token': auth_token,
            'refresh_token': refresh_token,
        }
        return self.get_response(message='Successfully Updated Password', result=result)


@view_authenticate_refresh()
class RenewAuthTokenView(APIViewMixin, generics.CreateAPIView):
    serializer_class = RenewAuthTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth_token = serializer.validated_data

        result = {
            'new_token': auth_token,
        }

        return self.get_response(message='Successfully Refreshed Token', result=result)


@view_authenticate_refresh()
class RenewRefreshTokenView(APIViewMixin, generics.CreateAPIView):
    serializer_class = RenewRefreshTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token, auth_token = serializer.validated_data

        result = {
            'refresh_token': refresh_token,
            'auth_token': auth_token,
        }

        return self.get_response(message='Successfully Refreshed Token', result=result)
