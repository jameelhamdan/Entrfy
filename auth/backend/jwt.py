from django.conf import settings
from datetime import datetime, timedelta
from auth.models import User
import jwt


TOKEN_EXPIRATION_PERIOD = settings.TOKEN_EXPIRATION_PERIOD
MAIN_SECRET_KEY = settings.SECRET_KEY


def get_secret_key(secret_key):
    return '{}_{}'.format(MAIN_SECRET_KEY, secret_key)


def decode_token(token, secret_key='', verify=True):
    try:
        # Decode Token
        token_data = jwt.decode(token, get_secret_key(secret_key), verify=verify, algorithms=['HS256'])
        return token_data

    except jwt.ExpiredSignatureError:
        raise Exception('Token Expired')


def create_auth_token(user_uuid, secret_key):
    expire_date = datetime.utcnow() + timedelta(days=TOKEN_EXPIRATION_PERIOD)

    # Create new auth token
    token = jwt.encode({'uuid': user_uuid, 'exp': expire_date}, get_secret_key(secret_key), algorithm='HS256', )
    return token


def verify_auth_token(token):
    try:
        # Auth User
        try:
            token_data = jwt.decode(token, verify=False)
            user_uuid = token_data['uuid']
            user = User.nodes.get(uuid=user_uuid)

            # Validate and Decode Token
            decode_token(token, user.secret_key)

            return user

        except User.DoesNotExist:
            raise Exception('This User Doesn\'t Exist!')

    except jwt.ExpiredSignatureError:
        raise Exception('This Token is expired!')


def refresh_auth_token(token, secret_key):
    token = decode_token(token, secret_key)
    user_uuid = token['uuid']
    return create_auth_token(user_uuid, secret_key)
