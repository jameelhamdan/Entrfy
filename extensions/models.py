from neomodel import (config, StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, DateTimeProperty)
from extensions.helpers import generate_uuid


class BaseNode(StructuredNode):
    __abstract_node__ = True
    uuid = UniqueIdProperty()
    created_on = DateTimeProperty(default_now=True)
    updated_on = DateTimeProperty(default_now=True)
