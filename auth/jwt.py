from django.conf import settings
import jwt
from datetime import datetime, timedelta
from auth.models import User

SECRET_KEY = settings.SECRET_KEY


def create_auth_token(user_uuid):
    encoded = jwt.encode({'uuid': user_uuid, 'exp': datetime.utcnow() + timedelta(days=30)}, settings.SECRET_KEY, algorithm='HS256', )
    return encoded


def verify_auth_token(token):
    try:
        # Decode Token
        data = jwt.decode(token, settings.SECRET_KEY, verify=True, algorithms=['HS256'])
        user_uuid = data['uuid']

        # Auth User
        try:
            User.nodes.get(uuid=user_uuid)
            data = data
            return True

        except User.DoesNotExist:
            return False
        except Exception as e:
            return False

    except jwt.ExpiredSignatureError:
        return False

    except Exception as e:
        return False
