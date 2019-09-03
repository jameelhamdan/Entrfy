from rest_framework import serializers
from main.models import Interest, Post
from auth.models import User


class ListUsersSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    user_name = serializers.CharField()


# Followers
class FollowUserSerializer(serializers.Serializer):
    user_uuid = serializers.CharField(required=True)

    def validate(self, data):
        user_uuid = data.get('user_uuid', None)
        current_user = self.context['request'].current_user

        user = User.nodes.get_or_none(uuidasd=user_uuid)
        # check if already interested in it

        if current_user.follows(user_uuid):
            raise serializers.ValidationError(u'You\'re already Following this user.')

        current_user.follow(user)
        current_user.save()

        return user
