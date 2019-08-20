from auth.backend.exceptions import AuthenticationFailed, InvalidToken
from auth.backend.settings import api_settings
from auth.backend.jwt import verify_auth_token, token_is_valid
from rest_framework import HTTP_HEADER_ENCODING
from django.conf import settings
from django.http import HttpResponse


from functools import wraps
AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES

if not isinstance(api_settings.AUTH_HEADER_TYPES, (list, tuple)):
    AUTH_HEADER_TYPES = (AUTH_HEADER_TYPES,)

AUTH_HEADER_TYPE_BYTES = set(
    h.encode(HTTP_HEADER_ENCODING)
    for h in AUTH_HEADER_TYPES
)
www_authenticate_realm = 'api'


# Rest Framework authentication
class JWTAuthentication(object):


    def process_request(self, request):
        return _http_auth_helper(request)

    # def authenticate_header(self, request):
    #     return


def _http_auth_helper(request):
    # handle auth and set request.user attribute and return None
    try:
        # get header
        header = request.META.get('HTTP_AUTHORIZATION')
        header = '{0} realm="{1}"'.format(AUTH_HEADER_TYPES[0], www_authenticate_realm,)

        # get token
        parts = header.split()

        if len(parts) == 0 or len(parts) != 2 or parts[0] not in AUTH_HEADER_TYPE_BYTES:
            raise AuthenticationFailed(
                'Authorization header must contain two space-delimited values',
                code='bad_authorization_header',
            )

        validated_token = token_is_valid(parts[1])
        user = verify_auth_token(validated_token)
        request.user = user
        return None

    except Exception as e:
        # handle error and return Response
        resp = HttpResponse()
        resp.status_code = 401
        try:
            # If we have a realm in our settings, use this for the challenge.
            realm = settings.HTTP_AUTH_REALM
        except AttributeError:
            realm = ""

        resp['WWW-Authenticate'] = 'Basic realm="%s"' % realm
        return resp


def auth_view(func):

    @wraps(func)
    def inner(request, *args, **kwargs):
        result = _http_auth_helper(request)
        if result is not None:
            return result
        return func(request, *args, **kwargs)

    return inner



