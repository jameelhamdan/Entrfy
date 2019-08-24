from neomodel import (config, StructuredNode, StringProperty, DateTimeProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom, Relationship, ZeroOrMore, ZeroOrOne, db)
from extensions.models import BaseNode, BaseReltionship
from extensions.helpers import hash_password, verify_password


class UserFollowerRelationship(BaseReltionship):
    pass


class UserInterestRelationship(BaseReltionship):
    pass


class UserPostRelationship(BaseReltionship):
    pass


class UserMixin(object):
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


class User(BaseNode, UserMixin):
    user_name = StringProperty(unique_index=True)
    email = StringProperty(unique_index=True)
    password_hash = StringProperty()
    last_login = DateTimeProperty(default_now=True)

    followers = Relationship('User', 'FOLLOWING', model=UserFollowerRelationship, cardinality=ZeroOrMore)
    interests = Relationship('main.models.Interest', "INTERESTED_IN", model=UserInterestRelationship, cardinality=ZeroOrMore)

    # check if this user follows another user
    def follows(self, user_uuid):
        query = "MATCH (a:User) WHERE a.uuid ='{}' MATCH (a)-[:FOLLOWING]->(b:User) WHERE b.uuid='{}' RETURN b LIMIT 1".format(user_uuid, self.uuid)
        results, meta = db.cypher_query(query)
        result = [User.inflate(row[0]) for row in results]
        return len(result) > 0

    # check if this user is being followed by other
    def followed_by(self, user_uuid):
        query = "MATCH (a:User) WHERE a.uuid ='{}' MATCH (a)-[:FOLLOWING]->(b:User) WHERE b.uuid='{}' RETURN b LIMIT 1".format(self.uuid, user_uuid)
        results, meta = db.cypher_query(query)
        result = [User.inflate(row[0]) for row in results]

        return len(result) > 0

    @property
    def get_followers(self):
        query = "MATCH (a:User) WHERE a.uuid ='{}' MATCH (a)-[:FOLLOWING]->(b:User) RETURN b".format(self.uuid)
        results, meta = db.cypher_query(query)
        people = [User.inflate(row[0]) for row in results]
