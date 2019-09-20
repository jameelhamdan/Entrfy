from neomodel import (StructuredNode, UniqueIdProperty, StructuredRel, DateTimeProperty)
import mongoengine as mongo
from datetime import datetime


class BaseNode(StructuredNode):
    __abstract_node__ = True
    uuid = UniqueIdProperty()
    created_on = DateTimeProperty(default_now=True)
    updated_on = DateTimeProperty(default_now=True)


class BaseReltionship(StructuredRel):

    created_on = DateTimeProperty(default_now=True)
    updated_on = DateTimeProperty(default_now=True)


class DocumentBase(mongo.Document):
    uuid = mongo.UUIDField(binary=False, unique=True)
    created_on = mongo.DateTimeField(default=datetime.utcnow)
    meta = {'allow_inheritance': True}


class EmbDocumentBase(mongo.EmbeddedDocument):
    uuid = mongo.UUIDField(binary=False)
    created_on = mongo.DateTimeField(default=datetime.utcnow)
    meta = {'allow_inheritance': True}
