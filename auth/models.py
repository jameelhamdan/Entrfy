from neomodel import (config, StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, DateTimeProperty)
from extensions.models import BaseNode


class User(BaseNode):
    user_name = StringProperty(unique_index=True)
    email = StringProperty(unique_index=True)
    password_hash = StringProperty()
    last_login = DateTimeProperty(default_now=True)
