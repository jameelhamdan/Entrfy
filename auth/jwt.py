from django.conf import settings
import jwt
from datetime import datetime, timedelta
from auth.models import User

SECRET_KEY = settings.SECRET_KEY


def create_auth_token(user_uuid):
    encoded = jwt.encode({'uuid': user_uuid, 'exp': datetime.utcnow() + timedelta(days=30)}, settings.SECRET_KEY, algorithm='HS256', )
    return encoded


def token_is_valid(token):
    try:
        # Decode Token
        jwt.decode(token, settings.SECRET_KEY, verify=True, algorithms=['HS256'])
        return token

    except jwt.ExpiredSignatureError:
        return Exception('This Token is expired!')

    except Exception as e:
        return Exception(str(e))


def verify_auth_token(token):
    try:
        # Decode Token
        data = jwt.decode(token, settings.SECRET_KEY, verify=True, algorithms=['HS256'])
        user_uuid = data['uuid']

        # Auth User
        try:
            user = User.nodes.get(uuid=user_uuid)
            return user

        except User.DoesNotExist:
            raise Exception('This User Doesn\'t Exist!')
        except Exception as e:
            raise e

    except jwt.ExpiredSignatureError:
        return Exception('This Token is expired!')

    except Exception as e:
        return Exception(str(e))
