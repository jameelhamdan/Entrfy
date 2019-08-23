from rest_framework import exceptions, status, views
from extensions.helpers import get_response


class APIViewMixin(views.APIView):
    # used to wrap exceptions with 'standard' message
    def handle_exception(self, exc):
        response = super(APIViewMixin, self).handle_exception(exc)

        response.data = {
            'success': False,
            'code': exc.default_code,
            'message': response.reason_phrase,
            'result': response.data
        }

        return response

    def get_response(self, success=True, message='Success', result=None, detail_code='success', status_code=status.HTTP_200_OK):
        return get_response(success=success, message=message, result=result, detail_code=detail_code, status_code=status_code)
