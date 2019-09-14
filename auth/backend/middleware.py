from rest_framework import status
from auth.backend.jwt import verify_auth_token, token_is_valid
from extensions.helpers import get_raw_response
from auth.backend.utils import AuthException, get_auth_header


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
        except AuthException as e:
            return get_raw_response(success=False, message='Authentication Failed', detail_code='authentication_failed', status_code=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            raise e

    def __call__(self, request):
        response = self.get_response(request)
        return response


def _http_auth_helper(request):
    try:
        token = get_auth_header(request)
        validated_token = token_is_valid(token)
        user = verify_auth_token(validated_token)

    except Exception as e:
        raise AuthException(e)

    return user
