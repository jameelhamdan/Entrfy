from rest_framework import exceptions, status, views
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
        response = exception_handler(exc, context)

        if response is None:
            self.raise_uncaught_exception(exc)

        response.exception = True

        response.data = {
            'success': False,
            'code': exc.default_code,
            'message': response.reason_phrase,
            'result': response.data
        }

        return response

    def get_response(self, success=True, message='Success', result=None, detail_code='success', status_code=status.HTTP_200_OK):
        return get_response(success=success, message=message, result=result, detail_code=detail_code, status_code=status_code)
