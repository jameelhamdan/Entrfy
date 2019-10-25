from collections import namedtuple
from django.conf import settings
from django.utils.functional import SimpleLazyObject

VERIFY_TYPE_AUTH = 'auth'
VERIFY_TYPE_ANY = 'any'
VERIFY_TYPE_REFRESH = 'refresh'

VERIFY_TYPES = [
    VERIFY_TYPE_AUTH,
    VERIFY_TYPE_ANY,
    VERIFY_TYPE_REFRESH
]

DEFAULTS = {
    'AUTH_TOKEN_LIFETIME': getattr(settings, 'AUTH_TOKEN_EXPIRATION_PERIOD', 14),
    'REFRESH_TOKEN_LIFETIME': getattr(settings, 'REFRESH_TOKEN_EXPIRATION_PERIOD', 14),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'META_TYPE': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'uuid',
    'USER_ID_CLAIM': 'user_uuid',
    'VERIFY_TYPES': VERIFY_TYPES,
    'VERIFY_TYPE_AUTH': VERIFY_TYPE_AUTH,
    'VERIFY_TYPE_ANY': VERIFY_TYPE_ANY,
    'VERIFY_TYPE_REFRESH': VERIFY_TYPE_REFRESH
}


def get_api_settings():
    temp_dict = getattr(settings, 'JWT_AUTH_SETTINGS', DEFAULTS)

    return namedtuple("API_SETTINGS", temp_dict.keys())(*temp_dict.values())


api_settings = SimpleLazyObject(lambda: get_api_settings())
