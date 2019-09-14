from django.conf import settings
import jwt
from datetime import datetime, timedelta
from auth.models import User

SECRET_KEY = settings.SECRET_KEY
TOKEN_EXPIRATION_PERIOD = settings.TOKEN_EXPIRATION_PERIOD


def decode_token(token):
    token_data = jwt.decode(token, settings.SECRET_KEY, verify=True, algorithms=['HS256'])
    return token_data


def create_auth_token(user_uuid):
    # Create new auth token
    token = jwt.encode({'uuid': user_uuid, 'exp': datetime.utcnow() + timedelta(days=TOKEN_EXPIRATION_PERIOD)}, settings.SECRET_KEY, algorithm='HS256', )
    return token


def token_is_valid(token):
    try:
        # Decode Token
        decode_token(token)
        return token

    except jwt.ExpiredSignatureError:
        raise Exception('Token expired')

    except Exception as e:
        raise Exception(str(e))


def verify_auth_token(token):
    try:
        # Decode Token
        token = decode_token(token)
        user_uuid = token['uuid']

        # Auth User
        try:
            user = User.nodes.get(uuid=user_uuid)
            # user.is_authenticated = True
            return user

        except User.DoesNotExist:
            raise Exception('This User Doesn\'t Exist!')
        except Exception as e:
            raise e

    except jwt.ExpiredSignatureError:
        raise Exception('This Token is expired!')

    except Exception as e:
        raise Exception(str(e))


def refresh_auth_token(token):
    token = decode_token(token)
    user_uuid = token['uuid']
    return create_auth_token(user_uuid)
