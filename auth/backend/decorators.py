from functools import wraps
from auth.backend.settings import api_settings
from django.utils.decorators import method_decorator


def _auth_user(auth_type='api_settings.VERIFY_TYPE_AUTH'):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            return view_func(*args, **kwargs)

        wrapped_view.auth_type = auth_type

        return wraps(view_func)(wrapped_view)

    return decorator


def view_allow_any():
    return method_decorator(_auth_user(auth_type=api_settings.VERIFY_TYPE_ANY), name='dispatch')


def view_authenticate():
    return method_decorator(_auth_user(auth_type=api_settings.VERIFY_TYPE_AUTH), name='dispatch')


def view_authenticate_refresh():
    return method_decorator(_auth_user(auth_type=api_settings.VERIFY_TYPE_REFRESH), name='dispatch')
