from auth.backend.settings import api_settings
from rest_framework import HTTP_HEADER_ENCODING

AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES
META_TYPE = api_settings.META_TYPE

AUTH_HEADER_TYPE_BYTES = set(
    h.encode(HTTP_HEADER_ENCODING)
    for h in AUTH_HEADER_TYPES
)
www_authenticate_realm = 'api'


class AuthException(Exception):
    pass


def get_auth_header(request):
    try:
        header = request.META.get(META_TYPE, None)
        if not header:
            raise Exception('Token not provided')

        # get token
        try:
            parts = header.split()
        except:
            raise Exception('Token invalid')

        if len(parts) == 0 or len(parts) != 2 or parts[0].encode(HTTP_HEADER_ENCODING) not in AUTH_HEADER_TYPE_BYTES:
            raise Exception('Token invalid')

        return parts[1]

    except Exception as e:
        raise AuthException(e)
