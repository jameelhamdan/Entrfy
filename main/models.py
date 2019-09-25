from neomodel import (config, StructuredNode, StringProperty, DateTimeProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom, Relationship, ZeroOrMore, ZeroOrOne, db)
from extensions.models import BaseNode, BaseReltionship
from auth.models import (User, UserInterestRelationship)
from main.followers.models import *
from main.interests.models import *
from main.matching.models import *
