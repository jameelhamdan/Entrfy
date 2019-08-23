from rest_framework import serializers
from main.models import Interest, Post
from neomodel import db

# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dWlkIjoiOGY2YzYzMGI5NDY1NDc2ZDg2YjE1YmExOGM0YzM3OTkiLCJleHAiOjE1NjkxNDQwMTJ9.9SwFCc-Z_kDBdZFGThR-8Nye3aY0skV5P2gnodbU9Qc
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dWlkIjoiNWQ0YjZiMDhjMmMzNDU3NGE4MzQxZjg3MzBkODU5YWYiLCJleHAiOjE1NjkxNDYxNDF9.k3VfNkiKYrJQ_0MTzbBathe45qBT1AErDBGtwLQ7ARQ
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
        try:
            interest_uuid = data.get('interest_uuid', None)

            current_user = data.request.current_user

            interest = Interest.nodes.get_or_none(uuid=interest_uuid)
            # check if already interested in it
            result = interest.users.relationship(current_user)
            if result:
                raise Exception('You\'re already interested in this topic')

            interest.users.connect(current_user)
            interest.save()

        except Exception as e:
            raise serializers.ValidationError('Internal Server Error ' + str(e))

        return interest


class ListInterestSerializer(serializers.Serializer):
    uuid = serializers.CharField()
    name = serializers.CharField()
