from rest_framework import response, status
import uuid
import hashlib
import binascii
import os

def generate_uuid():
    return lambda: uuid.uuid4().hex


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def serializer_to_json(serializer_class, list_object):
    return serializer_class(list_object, many=True).data


def get_response(success=True, message='Success', result=None, status_code=status.HTTP_200_OK):
    result = {
        'success': success,
        'message': message,
        'result': result
    }
    return response.Response(result, status=status_code)