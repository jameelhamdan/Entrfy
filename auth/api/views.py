from rest_framework import views, generics
from django.urls import path
from auth.api.serializers import LoginSerializer, RegisterSerializer
from rest_framework import status
from rest_framework.response import Response
from auth.backend.jwt import create_auth_token
from auth.middleware import view_allow_any, view_authenticate


@view_allow_any()
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        user = serializer.validate(request.data)

        token = create_auth_token(user.uuid)

        result_data = {
            'success': False,
            'message': 'Log in Error',
            'result': None
        }

        if token:
            result_data = {
                'success': True,
                'message': 'Successfully Logged in',
                'result': {
                    'uuid': user.uuid,
                    'token': token
                }
            }

        return Response(result_data, status=status.HTTP_200_OK)


@view_allow_any()
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = serializer.validate(request.data)

        result_data = {
            'success': True,
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Successfully Registered User',
            'data': {
                'uuid': user.uuid
            }
        }

        return Response(result_data, status=status.HTTP_200_OK)


@view_authenticate()
class HelloView(views.APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.current_user
        content = {'message': 'Hello, {}!'.format(user.user_name)}
        return Response(content, status=status.HTTP_200_OK)


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('auth_test/', HelloView.as_view(), name='auth_test'),
]
