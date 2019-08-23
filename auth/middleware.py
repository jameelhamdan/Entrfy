from auth.backend.settings import api_settings
from auth.backend.jwt import verify_auth_token, token_is_valid
from rest_framework import HTTP_HEADER_ENCODING, status
from functools import wraps
from django.utils.decorators import method_decorator
from extensions.helpers import get_raw_response


AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES

if not isinstance(api_settings.AUTH_HEADER_TYPES, (list, tuple)):
    AUTH_HEADER_TYPES = (AUTH_HEADER_TYPES,)

AUTH_HEADER_TYPE_BYTES = set(
    h.encode(HTTP_HEADER_ENCODING)
    for h in AUTH_HEADER_TYPES
)
www_authenticate_realm = 'api'


class AuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def process_view(request, view_func, *view_args, **view_kwargs):
        try:
            if getattr(view_func, 'authenticate_request', None):
                user = _http_auth_helper(request)
                setattr(request, 'current_user', user)
            return view_func(request, *view_args, **view_kwargs)

        except Exception as e:
            return get_raw_response(success=False, message='Authentication Failed', detail_code='authentication_failed', status_code=status.HTTP_401_UNAUTHORIZED)

    def __call__(self, request):
        response = self.get_response(request)
        return response


def _http_auth_helper(request):
    # get header
    header = request.META.get('HTTP_AUTHORIZATION', None)
    if not header:
        raise Exception('Token not provided')

    # get token
    try:
        parts = header.split()
    except:
        raise Exception('Token invalid')

    if len(parts) == 0 or len(parts) != 2 or parts[0].encode(HTTP_HEADER_ENCODING) not in AUTH_HEADER_TYPE_BYTES:
        raise Exception('Token invalid')

    validated_token = token_is_valid(parts[1])
    user = verify_auth_token(validated_token)
    return user


def _auth_user(value=True):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            return view_func(*args, **kwargs)

        wrapped_view.authenticate_request = value
        return wraps(view_func)(wrapped_view)
    return decorator


def view_allow_any():
    return method_decorator(_auth_user(value=False), name='dispatch')


def view_authenticate():
    return method_decorator(_auth_user(value=True), name='dispatch')

