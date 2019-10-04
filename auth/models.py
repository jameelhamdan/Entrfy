from neomodel import (config, StructuredNode, StringProperty, DateTimeProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom, Relationship, ZeroOrMore, ZeroOrOne, db)
from _common.models import BaseNode, BaseReltionship
from _common.helpers import hash_password, verify_password, generate_uuid

DEFAULT_PAGE_SIZE = 10


class UserFollowerRelationship(BaseReltionship):
    pass


class UserInterestRelationship(BaseReltionship):
    pass


class UserMixin(object):
    def set_password(self, new_password):
        self.password_hash = hash_password(new_password)
        self.save()

    def validate_password(self, password):
        return verify_password(self.password_hash, password)

    def reset_secret_key(self):
        self.secret_key = generate_uuid(3)
        self.save()

    @staticmethod
    def exists(user_name, email):
        query = "MATCH (a:User) WHERE a.user_name= '{}' OR a.email='{}' RETURN count(a) > 0".format(user_name, email)
        results, meta = db.cypher_query(query)
        return results[0][0]

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
    secret_key = StringProperty(default=generate_uuid(3))
    last_login = DateTimeProperty(default_now=True)

    followers = Relationship('User', 'FOLLOWING', model=UserFollowerRelationship, cardinality=ZeroOrMore)
    interests = Relationship('main.models.Interest', "INTERESTED_IN", model=UserInterestRelationship, cardinality=ZeroOrMore)

    # check if this user follows another user
    def follows(self, user_uuid):
        query = "MATCH (a:User) WHERE a.uuid ='{}' MATCH (a)-[:FOLLOWING]->(b:User) WHERE b.uuid='{}' RETURN b LIMIT 1".format(self.uuid, user_uuid)
        results, meta = db.cypher_query(query)
        result = [User.inflate(row[0]) for row in results]
        return len(result) > 0

    # check if this user is being followed by other
    def followed_by(self, user_uuid):
        query = "MATCH (a:User) WHERE a.uuid ='{}' MATCH (a)-[:FOLLOWING]->(b:User) WHERE b.uuid='{}' RETURN b LIMIT 1".format(user_uuid, self.uuid)
        results, meta = db.cypher_query(query)
        result = [User.inflate(row[0]) for row in results]

        return len(result) > 0

    # follow another user
    def follow(self, user):
        user.followers.connect(self)

        return user

    # get all users this users follow (maybe add pagination or something)
    @property
    def get_followed(self):
        query = "MATCH (a:User) WHERE a.uuid ='{}' MATCH (a)-[:FOLLOWING]->(b:User) RETURN b".format(self.uuid)
        results, meta = db.cypher_query(query)
        people = [User.inflate(row[0]) for row in results]

        return people

    def get_followed_paginate(self, page=1):
        page_size = DEFAULT_PAGE_SIZE
        current_skip = page * page_size
        query = "MATCH (a:User) WHERE a.uuid ='{}' MATCH (a)-[:FOLLOWING]->(b:User) RETURN b SKIP={} LIMIT={}".format(self.uuid, current_skip, page_size)
        results, meta = db.cypher_query(query)
        people = [User.inflate(row[0]) for row in results]

        return people

    def get_matches(self):
        query = "MATCH (p1:User {uuid:'%s'})-[:INTERESTED_IN]->(interests1) WITH p1, collect(id(interests1)) AS p1Interest " + \
                "MATCH (p2:User)-[:INTERESTED_IN]->(interests2) WITH p1, p2, algo.similarity.jaccard(p1Interest, collect(id(interests2))) AS similarity " + \
                "WHERE p1 <> p2 AND similarity > 0.1 RETURN p2.user_name AS name , p2.uuid AS uuid, similarity ORDER BY similarity DESC LIMIT 25;"

        query = query % self.uuid
        results, meta = db.cypher_query(query)
        return results
