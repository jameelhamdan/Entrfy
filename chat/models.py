from extensions.models import DocumentBase, EmbDocumentBase
from datetime import datetime
import mongoengine as mongo


class MessageNode(EmbDocumentBase):
    content = mongo.StringField(required=True, max_length=500)
    sent_by = mongo.StringField(required=True, max_length=36)
    sent_on = mongo.DateTimeField(default=datetime.utcnow)


class ChatNode(DocumentBase):
    users = mongo.ListField(mongo.StringField(max_length=36, unique=True))
    messages = mongo.EmbeddedDocumentListField(MessageNode)
    meta = {'collection': 'chat'}
