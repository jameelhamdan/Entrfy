from rest_framework import response, status
from django.http import JsonResponse
import uuid
import hashlib
import binascii
import os


def generate_uuid(repeat=1):
    final_uuid = ''
    for i in range(0, repeat):
        final_uuid += uuid.uuid4().hex

    return final_uuid


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'),  salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def serializer_to_json(serializer_class, list_object):
    return serializer_class(list_object, many=True).data


def get_response(success=True, message='Success', result=None, detail_code='success', status_code=status.HTTP_200_OK):
    result = {
        'success': success,
        'code': detail_code,
        'message': message,
        'result': result
    }
    return response.Response(result, status=status_code)


def get_raw_response(success=True, message='Success', result=None, detail_code='success', status_code=status.HTTP_200_OK):
    result = {
        'success': success,
        'code': detail_code,
        'message': message,
        'result': result
    }
    return JsonResponse(result, status=status_code)
