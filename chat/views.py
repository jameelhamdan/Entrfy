from rest_framework import generics
from django.urls import path
from chat.serializers import SendChatMessageSerializer, ChatMessagesSerializer
from auth.backend.decorators import view_allow_any, view_authenticate
from extensions.mixins import APIViewMixin


@view_authenticate()
class ListChatMessagesView(APIViewMixin, generics.ListAPIView):
    serializer_class = ChatMessagesSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.current_user
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        result = serializer.validated_data

        message = 'Successfully retrieved chat messages for chat'

        return self.get_response(message=message, result=result)


@view_authenticate()
class SendChatMessageView(APIViewMixin, generics.ListAPIView):
    serializer_class = SendChatMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        result = serializer.validated_data

        return self.get_response(message='Successfully Sent Message', result={'chat_uuid': result})


urlpatterns = [
    path('list_chat_messages/', ListChatMessagesView.as_view(), name='list_chat_messages'),
    path('send_chat_message/', SendChatMessageView.as_view(), name='send_chat_message'),
]
