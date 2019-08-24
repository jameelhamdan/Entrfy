from rest_framework import exceptions, status, views, response
from extensions.helpers import get_response


class APIViewMixin(views.APIView):
    def handle_exception(self, exc):
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN

        exception_handler = self.get_exception_handler()

        context = self.get_exception_handler_context()
        exc_response = exception_handler(exc, context)

        if exc_response is None:
            self.raise_uncaught_exception(exc)

            return response.Response({
                'success': False,
                'code': 'internal_server_error',
                'message': u'Internal Server Error',
                'result': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        exc_response.exception = True

        exc_response.data = {
            'success': False,
            'code': exc.default_code,
            'message': exc_response.reason_phrase,
            'result': exc_response.data
        }

        return exc_response

    def get_response(self, success=True, message='Success', result=None, detail_code='success', status_code=status.HTTP_200_OK):
        return get_response(success=success, message=message, result=result, detail_code=detail_code, status_code=status_code)
