from rest_framework import status
from extensions.helpers import get_raw_response


def handler404(request, *args, **argv):
    return get_raw_response(success=False, message='Page not Found', detail_code='page_not_found', status_code=status.HTTP_404_NOT_FOUND)


def handler500(request, *args, **argv):
    return get_raw_response(success=False, message='Internal Server Error', detail_code='internal_sever_error', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
