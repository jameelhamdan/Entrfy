from rest_framework import serializers
from auth.models import User
from auth.backend import jwt, utils
from auth.backend.jwt import create_auth_token, create_refresh_token


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

        user.update_last_login()
        auth_token = create_auth_token(user.uuid)
        refresh_token = create_refresh_token(user.uuid, user.secret_key)

        return user, auth_token, refresh_token


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


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        # Validate Password
        user = self.context['request'].current_user

        if not data['new_password'] == data['new_password_confirm']:
            raise serializers.ValidationError(u'Password Don\'t match!')

        if not user.validate_password(data['old_password']):
            raise serializers.ValidationError(u'Password Incorrect!')

        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError(u'New Password must be different than old password')

        user.set_password(data['new_password'])
        user.reset_secret_key()
        user.update_last_login()
        auth_token = create_auth_token(user.uuid)
        refresh_token = create_refresh_token(user.uuid, user.secret_key)

        return user, auth_token, refresh_token


class RenewAuthTokenSerializer(serializers.Serializer):
    def validate(self, data):
        user = self.context['request'].current_user

        old_token = utils.get_auth_header(self.context['request'])
        new_token = jwt.renew_auth_token(old_token, user.secret_key)
        return new_token


class RenewRefreshTokenSerializer(serializers.Serializer):
    def validate(self, data):
        user = self.context['request'].current_user
        
        old_token = utils.get_auth_header(self.context['request'])
        new_refresh_token = jwt.renew_refresh_token(old_token, user.secret_key)
        new_auth_token = jwt.renew_auth_token(old_token, user.secret_key)

        return new_refresh_token, new_auth_token
