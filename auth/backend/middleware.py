from auth.backend.jwt import verify_auth_token
from auth.backend.utils import AuthException, get_auth_header
from _common.errors import handler401


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
            return handler401(request, *view_args, **view_kwargs)

    def __call__(self, request):
        response = self.get_response(request)
        return response


def _http_auth_helper(request):
    try:
        token = get_auth_header(request)
        user = verify_auth_token(token)

    except Exception as e:
        raise AuthException(e)

    return user
