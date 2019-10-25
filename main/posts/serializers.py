from rest_framework import serializers
from main.models import mongo, PostDocument, CommentSubDocument, LikeSubDocument


class ListPostCommentsSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    content = serializers.CharField()
    created_by = serializers.CharField()
    created_on = serializers.DateTimeField()


class ListPostLikesSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    created_by = serializers.CharField()
    created_on = serializers.DateTimeField()


class ListPostsSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    content = serializers.CharField()
    posted_by = serializers.CharField()

    comments = ListPostCommentsSerializer(many=True)
    likes = ListPostLikesSerializer(many=True)
    created_on = serializers.DateTimeField()


class AddPostSerializer(serializers.Serializer):
    content = serializers.CharField(required=True, max_length=500)

    def validate(self, data):
        user_uuid = self.context['request'].current_user.uuid

        content = data.get('content', None)

        post = PostDocument(
            posted_by=user_uuid,
            content=content,
        ).save()

        return post.uuid


class AddPostCommentSerializer(serializers.Serializer):
    post_uuid = serializers.CharField(required=True, max_length=36)
    content = serializers.CharField(required=True, max_length=500)

    def validate(self, data):
        user_uuid = self.context['request'].current_user.uuid

        post_uuid = data.get('post_uuid', None)
        content = data.get('content', None)

        try:
            post = PostDocument.objects.get(uuid=post_uuid)
        except mongo.DoesNotExist:
            raise serializers.ValidationError({'post_uuid': [u'Post not found!']})

        comment = post.comment_on_post(user_uuid, content)

        return post.uuid, comment.uuid


class AddPostLikeSerializer(serializers.Serializer):
    post_uuid = serializers.CharField(required=True, max_length=36)

    def validate(self, data):
        user_uuid = self.context['request'].current_user.uuid

        post_uuid = data.get('post_uuid', None)

        # check if post exists
        try:
            post = PostDocument.objects.get(uuid=post_uuid)
        except mongo.DoesNotExist:
            raise serializers.ValidationError({'post_uuid': [u'Post not found!']})

        return post.uuid, post.like_post(user_uuid)
