from collections import namedtuple
from django.conf import settings
from django.utils.functional import SimpleLazyObject

DEFAULTS = {
    'TOKEN_LIFETIME': getattr(settings, 'TOKEN_EXPIRATION_PERIOD', 14),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'META_TYPE': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'uuid',
    'USER_ID_CLAIM': 'user_uuid',

}


def get_api_settings():
    temp_dict = getattr(settings, 'JWT_AUTH_SETTINGS', DEFAULTS)

    return namedtuple("API_SETTINGS", temp_dict.keys())(*temp_dict.values())


api_settings = SimpleLazyObject(lambda: get_api_settings())
