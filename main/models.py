from neomodel import (config, StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom, Relationship, ZeroOrMore, ZeroOrOne)
from extensions.models import BaseNode, BaseReltionship
from auth.models import User


class UserInterestRelationship(BaseReltionship):
    pass


class UserPostRelationship(BaseReltionship):
    pass


class Interest(BaseNode):
    name = StringProperty(unique_index=True, required=True)
    interested_users = Relationship(User, "INTERESTED_IN", model=UserInterestRelationship, cardinality=ZeroOrMore)


class Post(BaseNode):
    content = StringProperty(required=True)
    posted_by = RelationshipFrom(User, "POSTED", model=UserPostRelationship, cardinality=ZeroOrOne)
