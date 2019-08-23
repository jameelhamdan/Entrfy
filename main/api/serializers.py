from rest_framework import serializers
from main.models import Interest, Post


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
