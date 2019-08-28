from neomodel import (config, StructuredNode, StringProperty, DateTimeProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom, Relationship, ZeroOrMore, ZeroOrOne, db)
from extensions.models import BaseNode, BaseReltionship
from auth.models import (User, UserInterestRelationship, UserPostRelationship)


class Interest(BaseNode):
    name = StringProperty(unique_index=True, required=True)
    users = Relationship(User, "INTERESTED_IN", model=UserInterestRelationship, cardinality=ZeroOrMore)

    def interested_by(self, user_uuid):
        query = "MATCH (a:User) WHERE a.uuid ='{}' MATCH (a)-[:INTERESTED_IN]->(b:Interest) WHERE b.uuid='{}' RETURN b LIMIT 1".format(user_uuid, self.uuid)
        results, meta = db.cypher_query(query)
        result = [User.inflate(row[0]) for row in results]
        return len(result) > 0

    def interest_add(self, user):
        self.users.connect(user)
        return user

    @property
    def serialized(self):
        return {
            'name': self.name,
            'users': self.users
        }


class Post(BaseNode):
    content = StringProperty(required=True)
    posted_by = RelationshipFrom(User, "POSTED", model=UserPostRelationship, cardinality=ZeroOrOne)
