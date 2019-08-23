from rest_framework import serializers
from auth.models import User
from neomodel import Q


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    password = serializers.CharField(required=True)

    def validate(self, data):
        self.is_valid(raise_exception=True)

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
        self.is_valid(raise_exception=True)
        # Validate Password

        if not data['password'] == data['password_confirm']:
            raise serializers.ValidationError(u'Password Don\'t match!')

        # check for users with same email or user_name
        user_name = data['user_name']
        email = data['email']
        try:
            existing_user = User.nodes.filter(Q(Q(user_name=user_name) | Q(email=email))).first()
        except:
            existing_user = None

        if existing_user:
            if existing_user.email == email:
                raise serializers.ValidationError(u'This Email is already registered!')
            else:
                raise serializers.ValidationError(u'This Username is already registered!')
        try:
            user = User.create_user(
                user_name=data['user_name'],
                email=data['email'],
                password=data['password']
            )
        except Exception as e:
            raise serializers.ValidationError(u'Internal Server Error!')

        return user
