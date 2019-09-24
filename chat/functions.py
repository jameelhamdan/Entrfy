from chat.models import ChatNode, MessageNode
from auth.models import User
from neomodel import Q


def list_chats(user_uuid):
    chats = ChatNode.objects.filter(users__contains=user_uuid).order_by('-messages__sent_on')
    return chats


def create_chat(users_uuid):
    # check if uses exist
    new_chat_users = User.nodes.filter(Q(uuid__in=users_uuid))
    if len(new_chat_users) != len(users_uuid):
        raise Exception('Some Users Doesn\'t Exist!')

    chat = ChatNode(users=users_uuid)
    chat.save()

    return chat.uuid


def add_user_to_chat(chat_uuid, current_user, new_user_uuid):
    try:
        chat = ChatNode.objects.get(uuid=chat_uuid)
    except Exception as e:
        raise Exception('Chat not found!')

    if current_user not in chat.users:
        raise Exception('User is not in this chat')

    if new_user_uuid in chat.users:
        raise Exception('User already in this chat')

    # check if users exist

    new_chat_user = User.nodes.get_or_none(uuid=new_user_uuid)
    if not new_chat_user:
        raise Exception('User Doesn\'t Exist!')

    chat.users.append(new_user_uuid)
    chat.save()

    return chat_uuid


def send_message(chat_uuid, user_uuid, content):
    try:
        chat = ChatNode.objects.get(uuid=chat_uuid)
    except Exception as e:
        raise Exception('Chat not found!')

    if user_uuid not in chat.users:
        raise Exception('User is not in this chat')

    chat.messages.create(content=content, sent_by=user_uuid)
    chat.save()


def show_messages(chat_uuid, user_uuid, amount=10, skip=0, last_message_uuid=None):
    try:
        chat = ChatNode.objects.get(uuid=chat_uuid)
    except Exception as e:
        raise Exception('Chat not found! {}'.format(e))

    if user_uuid not in chat.users:
        raise Exception('User is not in this chat')

    return chat.messages[skip:amount]


def count_messages(chat_uuid, user_uuid):
    try:
        chat = ChatNode.objects.get(uuid=chat_uuid)
    except Exception as e:
        raise Exception('Chat not found!')

    if user_uuid not in chat.users:
        raise Exception('User is not in this chat')

    return chat.messages.count()
