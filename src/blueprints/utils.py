import json
import os
import re
from base64 import b64decode, b64encode

from Crypto.Cipher import ChaCha20
from dicttoxml import dicttoxml
from flask import jsonify
from sqlalchemy import create_engine

if os.environ.get('SECRET_KEY'):
    key = b64decode(os.environ.get('SECRET_KEY'))

def get_db_engine(data):
    host = 'localhost' if os.environ.get('FLASK_ENV') == 'development' else 'db'

    user = data.split(':')[0]
    password = data.split(':')[1]
    db_name = os.environ.get('DB_NAME')

    if not re.match(r'^[a-zA-Z0-9_]+$', user) or not re.match(r'^[a-zA-Z0-9_]+$', password):
        raise ValueError("Invalid username or password")

    return create_engine(f"postgresql+psycopg://{user}:{password}@{host}:5432/{db_name}",
                         echo=True, pool_size=20, max_overflow=0)

def generate_response(data, request, code=200):
    if request.headers.get('accept') == 'application/json':
        return jsonify(data), code
    elif request.headers.get('accept') == 'application/xml':
        return dicttoxml(data, custom_root='response', attr_type=False), code, {'Content-Type': 'application/xml'}
    else:
        return jsonify({"msg": "Invalid Accept header"}), 400

def encrypt(data):
    cipher = ChaCha20.new(key=key)

    nonce = b64encode(cipher.nonce).decode('utf-8')
    ciphertext = b64encode(cipher.encrypt(data.encode('utf-8'))).decode('utf-8')

    return json.dumps({'nonce': nonce, 'ciphertext': ciphertext})

def decrypt(data):
    nonce = b64decode(data['nonce'])
    ciphertext = b64decode(data['ciphertext'])

    cipher = ChaCha20.new(key=key, nonce=nonce)

    return cipher.decrypt(ciphertext).decode('utf-8')

def check_env_vars(vars_list):
    for var in vars_list:
        if os.getenv(var) is None:
            return False
    return True
