from rest_framework import serializers
from main.models import Interest, Post
from auth.models import User


class AddInterestSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)

    def validate(self, data):
        try:
            name = data.get('name', None)
            interest = Interest(name=name)
            interest.save()
            return interest
        except Exception as e:
            raise serializers.ValidationError(e.detail)


class AddUserInterestSerializer(serializers.Serializer):
    interest_uuid = serializers.CharField(required=True)

    def validate(self, data):
        try:
            interest_uuid = data.get('interest_uuid', None)
            current_user = self.context['request'].current_user

            interest = Interest.nodes.get_or_none(uuid=interest_uuid)
            # check if already interested in it
            result = interest.users.relationship(current_user)
            if result:
                raise serializers.ValidationError(u'You\'re already interested in this topic')

            interest.users.connect(current_user)
            interest.save()

            return interest
        except Exception as e:
            raise serializers.ValidationError(e.detail)


class ListInterestSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    name = serializers.CharField()


# Followers
class FollowUserSerializer(serializers.Serializer):
    user_uuid = serializers.CharField(required=True)

    def validate(self, data):
        try:
            user_uuid = data.get('user_uuid', None)
            current_user = self.context['request'].current_user

            user = User.nodes.get_or_none(uuid=user_uuid)
            # check if already interested in it

            if current_user.follows(user_uuid):
                raise serializers.ValidationError(u'You\'re already Following this user.')

            current_user.followers.connect(user)
            current_user.save()

            return user
        except Exception as e:
            raise serializers.ValidationError(e.detail)
