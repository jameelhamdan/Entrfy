from neomodel import (config, StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, DateTimeProperty)
from extensions.models import BaseNode
from extensions.helpers import hash_password, verify_password
from functools import partial


class User(BaseNode):
    user_name = StringProperty(unique_index=True)
    email = StringProperty(unique_index=True)
    password_hash = StringProperty()
    last_login = DateTimeProperty(default_now=True)

    # @property
    # def is_authenticated(self):
    #     return self.is_authenticated
    #
    # @is_authenticated.setter
    # def is_authenticated(self, value):
    #     self.is_authenticated = value

    def set_password(self, new_password):
        self.password_hash = hash_password(new_password)
        self.save()

    def validate_password(self, password):
        return verify_password(self.password_hash, password)

    @staticmethod
    def create_user(user_name, email, password):
        try:
            new_user = User(user_name=user_name, email=email)
            new_user.save()
            new_user.set_password(password)
            return new_user
        except Exception as e:
            return None
