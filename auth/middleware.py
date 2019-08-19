from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework import HTTP_HEADER_ENCODING
from auth.jwt import verify_auth_token, token_is_valid


AUTH_HEADER_TYPES = api_settings.AUTH_HEADER_TYPES

if not isinstance(api_settings.AUTH_HEADER_TYPES, (list, tuple)):
    AUTH_HEADER_TYPES = (AUTH_HEADER_TYPES,)

AUTH_HEADER_TYPE_BYTES = set(
    h.encode(HTTP_HEADER_ENCODING)
    for h in AUTH_HEADER_TYPES
)


# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dWlkIjoiOGY2YzYzMGI5NDY1NDc2ZDg2YjE1YmExOGM0YzM3OTkiLCJleHAiOjE1Njg3ODY0NjV9.vR1J_LfygoeziZ9axDvRGRkes12-l35t45BJXtuFf-U
class JWTAuthentication:
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)
        result = self.get_user(validated_token)
        if type(result) is Exception:
            raise AuthenticationFailed(result)

        return result, None

    def authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def get_header(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')

        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header):
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in AUTH_HEADER_TYPE_BYTES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise AuthenticationFailed(
                'Authorization header must contain two space-delimited values',
                code='bad_authorization_header',
            )

        return parts[1]

    def get_validated_token(self, raw_token):
        try:
            return token_is_valid(raw_token)

        except Exception as e:
            raise InvalidToken({
                'detail': 'Invalid Token',
                'message': str(e)
            })

    def get_user(self, raw_token):
        try:
            return verify_auth_token(raw_token)
        except Exception as e:
            raise InvalidToken({
                'detail': 'Token Invalid: {}'.format(e),
            })
