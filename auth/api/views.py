from rest_framework import views, generics
from django.urls import path
from auth.api.serializers import LoginSerializer, RegisterSerializer
from auth.models import User
from rest_framework import status
from rest_framework.response import Response
from auth.backend.jwt import create_auth_token
from rest_framework.permissions import IsAuthenticated


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
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Successfully Registered User',
            'data': {
                'uuid': user.uuid
            }
        }

        return Response(result_data, status=status.HTTP_201_CREATED)


class HelloView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        content = {'message': 'Hello, {}!'.format(request.user.user_name)}
        return Response(content)


urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('auth_test', HelloView.as_view(), name='auth_test'),
]
