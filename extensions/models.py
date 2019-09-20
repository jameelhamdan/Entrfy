from neomodel import (StructuredNode, UniqueIdProperty, StructuredRel, DateTimeProperty)


class BaseNode(StructuredNode):
    __abstract_node__ = True
    uuid = UniqueIdProperty()
    created_on = DateTimeProperty(default_now=True)
    updated_on = DateTimeProperty(default_now=True)


class BaseReltionship(StructuredRel):

    created_on = DateTimeProperty(default_now=True)
    updated_on = DateTimeProperty(default_now=True)
