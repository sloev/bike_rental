__author__ = 'johannes'
from base64 import b64encode
import os
from hashlib import sha256
import logging

def create_password_from_clear( password):
    salt = b64encode(os.urandom(16))
    _password = _encrypt_password(salt, password)
    return salt, _password

def authenticate(stored_password, stored_salt, new_password):

    _new_password = _encrypt_password(stored_salt, new_password)
    logging.info("auth - authenticate: stored_password=%s, stored_salt=%s, new_password=%s, _new=%s" %(stored_password, stored_salt, new_password, _new_password))
    return _new_password == stored_password

def _encrypt_password(salt, password):

    if isinstance(password, str):
        password_bytes = password.encode("UTF-8")
    else:
        password_bytes = password

    hashed_password = sha256()
    hashed_password.update(password_bytes)
    hashed_password.update(salt)
    hashed_password = hashed_password.hexdigest()
    if not isinstance(hashed_password, str):
        hashed_password = hashed_password.decode("UTF-8")
    return hashed_password