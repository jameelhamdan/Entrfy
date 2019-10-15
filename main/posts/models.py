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

    content = mongo.StringField(required=True, max_length=500)

    posted_by = mongo.StringField(max_length=36)
    comments = mongo.EmbeddedDocumentListField(CommentSubDocument)
    likes = mongo.EmbeddedDocumentListField(LikeSubDocument)

    created_on = mongo.DateTimeField(default=datetime.utcnow)

    def comment_on_post(self, user_uuid, content):
        comment = self.comments.create(content=content, created_by=user_uuid)
        self.save()
        return comment

    def like_post(self, user_uuid):
        # if like exists remove it if it doesn't add it
        if self.likes.filter(created_by=user_uuid).count():

            self.likes.filter(created_by=user_uuid).delete()
            like_added = False
        else:

            self.likes.create(created_by=user_uuid)
            like_added = True

        self.save()
        return like_added

    meta = {
        'collection': 'post',
    }
