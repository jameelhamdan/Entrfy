from rest_framework import serializers
from auth.models import User
from neomodel import Q


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user_name = data.get('user_name', None)
        email = data.get('email', None)

        user = None

        if not user_name and not email:
            raise serializers.ValidationError(u'You must provide an email or username')

        if user_name and email:
            raise serializers.ValidationError(u'You must only provide email or username not both')

        if user_name:
            user = User.nodes.get_or_none(user_name=user_name)

        elif email:
            user = User.nodes.get_or_none(email=email)

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

        if User.exists(user_name, email):
            raise serializers.ValidationError(u'This Email or Username is already registered!')

        user = User.create_user(
            user_name=data['user_name'],
            email=data['email'],
            password=data['password']
        )

        return user
