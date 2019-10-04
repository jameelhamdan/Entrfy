from datetime import datetime
from _common.helpers import generate_uuid
import mongoengine as mongo


class CommentSubDocument(mongo.EmbeddedDocument):
    uuid = mongo.StringField(max_length=36, default=generate_uuid)
    content = mongo.StringField(required=True, max_length=500)

    created_by = mongo.StringField(required=True, max_length=36)
    created_on = mongo.DateTimeField(default=datetime.utcnow)


class LikeSubDocument(mongo.EmbeddedDocument):
    uuid = mongo.StringField(max_length=36, default=generate_uuid)

    created_by = mongo.StringField(required=True, max_length=36)
    created_on = mongo.DateTimeField(default=datetime.utcnow)


class PostDocument(mongo.Document):
    uuid = mongo.StringField(max_length=36, default=generate_uuid, unique=True)
    posted_by = mongo.ListField(mongo.StringField(max_length=36))

    comments = mongo.EmbeddedDocumentListField(CommentSubDocument)
    likes = mongo.EmbeddedDocumentListField(LikeSubDocument)

    created_on = mongo.DateTimeField(default=datetime.utcnow)
    meta = {
        'collection': 'post',
    }
