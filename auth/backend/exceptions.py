from rest_framework import exceptions, status


class TokenError(Exception):
    pass


class TokenBackendError(Exception):
    pass


class DetailDictMixin:
    default_detail = 'Internal Server Error'
    default_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, detail=None, code=None):
        detail_dict = {
            'success': False,
            'message': self.default_detail,
            'code': self.default_code,
            'result': None
        }

        if isinstance(detail, dict):
            detail_dict.update(detail)

        elif detail is not None:
            detail_dict['message'] = detail

        if code is not None:
            detail_dict['code'] = code

        super().__init__(detail_dict)


class AuthenticationFailed(DetailDictMixin, exceptions.AuthenticationFailed):
    pass


class InvalidToken(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Token is invalid or expired'
    default_code = 'token_not_valid'
