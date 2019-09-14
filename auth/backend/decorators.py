from functools import wraps
from django.utils.decorators import method_decorator


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