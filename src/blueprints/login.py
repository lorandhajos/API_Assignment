import os

from flask import request
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import Schema, fields

from .utils import encrypt, generate_response, get_db_engine

class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

class LoginResponseSchema(Schema):
    access_token = fields.String(required=True)
    refresh_token = fields.String(required=True)

class Login(MethodView):
    def post(self):
        """
        Login
        ---
        tags:
            - login
        description: Login endpoint
        requestBody:
            content:
                application/json:
                    schema: LoginSchema
        responses:
            200:
                description: Login successful
                content:
                    application/json:
                        schema: LoginResponseSchema
                    application/xml:
                        schema: LoginResponseSchema
            400:
                description: Invalid Accept header
                content:
                    application/json:
                        schema: ErrorResponseSchema
                    application/xml:
                        schema: ErrorResponseSchema
            401:
                description: Bad username or password
                content:
                    application/json:
                        schema: ErrorResponseSchema
                    application/xml:
                        schema: ErrorResponseSchema
        """
        try:
            username = request.json.get('username')
            password = request.json.get('password')

            if os.environ.get('FLASK_ENV') != 'development':
                if username == os.environ.get('DB_USER') and password == os.environ.get('DB_PASS'):
                    raise ValueError("Invalid username or password")

            data = f"{username}:{password}"

            engine = get_db_engine(data)
            engine.connect()

            result = encrypt(data)
        except Exception:
            return generate_response({"msg": "Bad username or password"}, request, 401)

        access_token = create_access_token(identity=result)
        refresh_token = create_refresh_token(identity=result)

        return generate_response({"access_token": access_token, "refresh_token": refresh_token},
                                 request)
