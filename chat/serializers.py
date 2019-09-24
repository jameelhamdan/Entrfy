from rest_framework import serializers
from chat import functions
from extensions.helpers import serializer_to_json
from neomodel import Q


class UUIDSerializer(serializers.Serializer):
    uuid =serializers.CharField(required=True)


class ListChatMessagesSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    content = serializers.CharField()
    sent_by = serializers.CharField()
    sent_on = serializers.DateTimeField()


class ChatMessagesSerializer(serializers.Serializer):
    chat_uuid = serializers.CharField(required=True)

    def validate(self, data):
        chat_uuid = data.get('user_uuid', None)
        content = data.get('content', None)

        current_user = self.context['request'].current_user
        chat_messages = functions.show_messages(chat_uuid, current_user.uuid)

        chat_messages_json = serializer_to_json(ListChatMessagesSerializer, chat_messages)

        return chat_messages_json


# Followers
class SendChatMessageSerializer(serializers.Serializer):
    chat_uuid = serializers.CharField(required=True)
    content = serializers.CharField(required=True)

    def validate(self, data):
        chat_uuid = data.get('user_uuid', None)
        content = data.get('content', None)

        current_user = self.context['request'].current_user
        functions.send_message(chat_uuid, current_user.uuid, content)

        return chat_uuid


class AddChatSerializer(serializers.Serializer):
    user_uuid_list = serializers.ListField(child=serializers.CharField(required=True))

    def validate(self, data):
        user_uuid_list = data.get('user_uuid_list', None)
        current_user = self.context['request'].current_user
        if user_uuid_list:
            user_uuid_list = list(set(user_uuid_list).add(current_user.uuid))
        else:
            user_uuid_list = [current_user.uuid]

        chat_uuid = functions.create_chat(user_uuid_list)

        return chat_uuid
