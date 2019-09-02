from rest_framework import serializers
from main.models import Interest, Post
from auth.models import User


class AddInterestSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)

    def validate(self, data):
        name = data.get('name', None)
        interest = Interest(name=name)
        interest.save()
        return interest


class AddUserInterestSerializer(serializers.Serializer):
    interest_uuid = serializers.CharField(required=True)

    def validate(self, data):
        interest_uuid = data.get('interest_uuid', None)
        current_user = self.context['request'].current_user

        interest = Interest.nodes.get_or_none(uuid=interest_uuid)
        # check if already interested in it

        if interest.interested_by(current_user.uuid):
            raise serializers.ValidationError(u'You\'re already interested in this topic')

        interest.interest_add(current_user)

        return interest


class ListInterestSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    name = serializers.CharField()


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

