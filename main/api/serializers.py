from rest_framework import serializers
from main.models import Interest, Post
from neomodel import db


class AddInterestSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)

    def validate(self, data):
        self.is_valid(raise_exception=True)

        name = data.get('name', None)
        interest = Interest(name=name)
        interest.save()

        return interest


class AddUserInterestSerializer(serializers.Serializer):
    interest_uuid = serializers.CharField(required=True)

    def validate(self, data):
        self.is_valid(raise_exception=True)

        interest_uuid = data.get('interest_uuid', None)

        current_user = data.request.current_user

        interest = Interest.nodes.get_or_none(uuid=interest_uuid)
        # check if already interested in it
        result = interest.users.relationship(current_user)
        if result:
            raise Exception('You\'re already interested in this topic')

        interest.users.connect(current_user)
        interest.save()

        return interest


class ListInterestSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    name = serializers.CharField()
