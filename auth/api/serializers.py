from rest_framework import serializers
from auth.models import User


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = User.nodes.get_or_none(user_name=data['user_name'])

        if user is None or not user.validate_password(data['password']):
            raise serializers.ValidationError(u'Password or username is incorrect')

        return user


class RegisterSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        # Validate Password

        if not data['password'] == data['password_confirm']:
            raise serializers.ValidationError(u'Password Don\'t match!')

        # check for users with same email or user_name
        user_name = data['user_name']
        email = data['email']

        if User.nodes.first_or_none(user_name=user_name):
            raise serializers.ValidationError(u'This User name is already registered!')

        if User.nodes.first_or_none(email=email):
            raise serializers.ValidationError(u'This email is already registered!')

        return data
