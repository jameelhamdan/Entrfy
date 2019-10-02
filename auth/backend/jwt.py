from auth.backend.settings import api_settings
from datetime import datetime, timedelta
from auth.models import User
import jwt


TOKEN_EXPIRATION_PERIOD = timedelta(api_settings.TOKEN_LIFETIME)
MAIN_SECRET_KEY = api_settings.SIGNING_KEY
user_id_field = api_settings.USER_ID_FIELD


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
    expire_date = datetime.utcnow() + TOKEN_EXPIRATION_PERIOD

    # Create new auth token
    token = jwt.encode({user_id_field: user_uuid, 'exp': expire_date}, get_secret_key(secret_key), algorithm=api_settings.ALGORITHM, )
    return token


def verify_auth_token(token):
    try:
        # Auth User
        try:
            token_data = jwt.decode(token, verify=False)
            user_uuid = token_data[user_id_field]
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
    user_uuid = token[user_id_field]
    return create_auth_token(user_uuid, secret_key)
