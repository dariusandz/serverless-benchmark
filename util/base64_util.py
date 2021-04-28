import base64


def decode_base64(source):
    base64_bytes = source.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('ascii')
