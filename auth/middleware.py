from auth.backend.exceptions import AuthenticationFailed
from auth.backend.settings import api_settings
from auth.backend.jwt import verify_auth_token, token_is_valid
from rest_framework import HTTP_HEADER_ENCODING
from django.conf import settings
from django.http import HttpResponse
from re import sub
from functools import wraps
from django.middleware.common import MiddlewareMixin

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
            if view_func.authenticate_request:
                header_token = request.META.get('HTTP_AUTHORIZATION', None)
                if header_token is not None:
                    user = _http_auth_helper(request)
                    setattr(request, 'current_user', user)
                    return view_func(request, *view_args, **view_kwargs)

        except Exception as e:
            return view_func(request, *view_args, **view_kwargs)

    def __call__(self, request):
        response = self.get_response(request)
        return response


def _http_auth_helper(request):
    # handle auth and set request.user attribute and return None
    try:
        # get header
        header = request.META.get('HTTP_AUTHORIZATION', None)

        # get token
        parts = header.split()

        if len(parts) == 0 or len(parts) != 2 or parts[0].encode(
                HTTP_HEADER_ENCODING) not in AUTH_HEADER_TYPE_BYTES:
            raise AuthenticationFailed(
                'Authorization header must contain two space-delimited values',
                code='bad_authorization_header',
            )

        validated_token = token_is_valid(parts[1])
        user = verify_auth_token(validated_token)
        return user

    except Exception as e:
        resp = HttpResponse()
        resp.status_code = 401
        try:
            realm = settings.HTTP_AUTH_REALM
        except AttributeError:
            realm = ""

        resp['WWW-Authenticate'] = 'Basic realm="%s"' % realm
        return resp


def auth_view(function):
    orig_func = function
    setattr(orig_func, 'authenticate_request', True)
    return function
