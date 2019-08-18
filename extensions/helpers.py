import uuid


def generate_uuid():
    return lambda: uuid.uuid4().hex

