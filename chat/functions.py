from rest_framework import serializers
from chat.models import ChatDocument, mongo
from auth.models import User
from neomodel import Q


def list_chats(user_uuid):
    chats = ChatDocument.objects.filter(users__contains=user_uuid).order_by('-messages__sent_on')
    return chats


def create_chat(users_uuid):
    # check if uses exist
    new_chat_users = User.nodes.filter(Q(uuid__in=users_uuid))
    if len(new_chat_users) != len(users_uuid):
        raise serializers.ValidationError({'user_uuid_list': [u'Some Users Doesn\'t Exist!']})

    chat = ChatDocument(users=users_uuid)
    chat.save()

    return chat.uuid


def add_user_to_chat(chat_uuid, current_user, new_user_uuid):
    chat = ChatDocument.objects.get(uuid=chat_uuid)

    if not chat:
        raise serializers.ValidationError({'chat_uuid': [u'Chat not found!']})

    if current_user not in chat.users:
        raise serializers.ValidationError(u'User is not in this chat')

    if new_user_uuid in chat.users:
        raise serializers.ValidationError({'user_uuid': [u'User already in this chat']})

    # check if users exist
    new_chat_user = User.nodes.get(uuid=new_user_uuid)
    if not new_chat_user:
        raise serializers.ValidationError({'user_uuid': [u'User Doesn\'t Exist!']})

    chat.users.append(new_user_uuid)
    chat.save()

    return chat_uuid


def send_message(chat_uuid, user_uuid, content):
    try:
        chat = ChatDocument.objects.get(uuid=chat_uuid)
    except mongo.DoesNotExist:
        raise serializers.ValidationError({'chat_uuid': [u'Chat not found!']})

    if user_uuid not in chat.users:
        raise serializers.ValidationError(u'User is not in this chat')

    chat.messages.create(content=content, sent_by=user_uuid)
    chat.save()


def show_messages(chat_uuid, user_uuid, amount=10, skip=0, last_message_uuid=None):
    try:
        chat = ChatDocument.objects.get(uuid=chat_uuid)
    except mongo.DoesNotExist:
        raise serializers.ValidationError({'chat_uuid': [u'Chat not found!']})

    if user_uuid not in chat.users:
        raise serializers.ValidationError(u'User is not in this chat')

    return chat.messages[skip:amount]


def count_messages(chat_uuid, user_uuid):
    try:
        chat = ChatDocument.objects.get(uuid=chat_uuid)
    except mongo.DoesNotExist:
        raise serializers.ValidationError({'chat_uuid': [u'Chat not found!']})

    if user_uuid not in chat.users:
        raise serializers.ValidationError(u'User is not in this chat')

    return chat.messages.count()
