from chat.models import ChatNode, MessageNode


def create_chat(users_uuid):
    chat = ChatNode(users=users_uuid)
    chat.save()

    return chat.uuid


def add_user_to_chat(chat_uuid, user_uuid):
    chat = ChatNode.objects.get(uuid=chat_uuid)
    chat.users.append(user_uuid)
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
