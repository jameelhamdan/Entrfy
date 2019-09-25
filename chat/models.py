from datetime import datetime
from extensions.helpers import generate_uuid
import mongoengine as mongo


class MessageSubDocument(mongo.EmbeddedDocument):
    uuid = mongo.StringField(max_length=36, default=generate_uuid)

    content = mongo.StringField(required=True, max_length=500)
    sent_by = mongo.StringField(required=True, max_length=36)
    sent_on = mongo.DateTimeField(default=datetime.utcnow)

    created_on = mongo.DateTimeField(default=datetime.utcnow)


class ChatDocument(mongo.Document):
    uuid = mongo.StringField(max_length=36, default=generate_uuid, unique=True)

    users = mongo.ListField(mongo.StringField(max_length=36))
    messages = mongo.EmbeddedDocumentListField(MessageSubDocument)

    created_on = mongo.DateTimeField(default=datetime.utcnow)
    meta = {
        'collection': 'chat',
    }
