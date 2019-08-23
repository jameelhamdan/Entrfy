from neomodel import (config, StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom, Relationship, ZeroOrMore, ZeroOrOne)
from extensions.models import BaseNode, BaseReltionship
from auth.models import (User, UserInterestRelationship, UserPostRelationship)


class Interest(BaseNode):
    name = StringProperty(unique_index=True, required=True)
    users = Relationship(User, "INTERESTED_IN", model=UserInterestRelationship, cardinality=ZeroOrMore)

    @property
    def serialized(self):
        return {
            'name': self.name,
            'users': self.users
        }


class Post(BaseNode):
    content = StringProperty(required=True)
    posted_by = RelationshipFrom(User, "POSTED", model=UserPostRelationship, cardinality=ZeroOrOne)
