from auth.backend.settings import api_settings
from auth.backend.jwt import verify_auth_token, token_is_valid
from rest_framework import HTTP_HEADER_ENCODING, status
from django.http import JsonResponse


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

            result_data = {
                'success': False,
                'message': 'Authentication Error',
                'result': str(e)
            }

            return JsonResponse(result_data, status=status.HTTP_401_UNAUTHORIZED)

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


def auth_view(method_name='dispatch'):
    def inner(cls):
        orig_func = getattr(cls, method_name)
        setattr(orig_func, 'authenticate_request', True)
        setattr(cls, method_name, orig_func)
        
        return cls
    return inner
