from rest_framework import generics
from django.urls import path
from chat.serializers import *
from auth.backend.decorators import view_allow_any, view_authenticate
from extensions.mixins import APIViewMixin


@view_authenticate()
class ListChatsView(APIViewMixin, generics.ListAPIView):
    serializer_class = UserChatsSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        result = serializer.validated_data

        message = 'Successfully retrieved current user chats'

        return self.get_response(message=message, result=result)


@view_authenticate()
class ListChatMessagesView(APIViewMixin, generics.ListAPIView):
    serializer_class = ChatMessagesSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        result = serializer.validated_data

        message = 'Successfully retrieved chat messages for chat'

        return self.get_response(message=message, result=result)


@view_authenticate()
class SendChatMessageView(APIViewMixin, generics.CreateAPIView):
    serializer_class = SendChatMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        result = serializer.validated_data

        return self.get_response(message='Successfully Sent Message', result={'chat_uuid': result})


@view_authenticate()
class AddChatView(APIViewMixin, generics.CreateAPIView):
    serializer_class = AddChatSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        result = serializer.validated_data

        return self.get_response(message='Successfully Added Chat', result={'chat_uuid': result})


@view_authenticate()
class AddUserToChatView(APIViewMixin, generics.CreateAPIView):
    serializer_class = AddUserToChatSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        result = serializer.validated_data

        return self.get_response(message='Successfully User To Chat', result={'chat_uuid': result})


urlpatterns = [
    path('list_chats/', ListChatsView.as_view(), name='list_chats'),
    path('list_chat_messages/', ListChatMessagesView.as_view(), name='list_chat_messages'),
    path('send_chat_message/', SendChatMessageView.as_view(), name='send_chat_message'),
    path('add_chat/', AddChatView.as_view(), name='add_chat'),
    path('add_user_to_chat/', AddUserToChatView.as_view(), name='add_user_to_chat'),
]
