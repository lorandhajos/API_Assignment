import os

import bcrypt
from flask import request
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import Schema, fields
from sqlalchemy.sql import text

from .utils import encrypt, generate_response, get_db_engine

class UserLoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)

class UserLogin(MethodView):
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
                    schema: UserLoginSchema
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
            data = f"{os.environ.get('API_USER_NAME')}:{os.environ.get('API_USER_PASS')}"

            email = request.json.get('email')
            password = request.json.get('password')

            engine = get_db_engine(data)
            with engine.connect() as connection:
                data = connection.execute(text("SELECT account_id, password FROM selectLogin WHERE email = :email;"),
                                             {"email": email, "password": password}).first()

            if not bcrypt.checkpw(password.encode('utf-8'), data[1].encode('utf-8')):
                return generate_response({"msg": "Bad username or password"}, request, 401)

            result = encrypt(f"{data}:{data[0]}")
        except Exception as e:
            print(e)
            return generate_response({"msg": "Bad username or password"}, request, 401)

        access_token = create_access_token(identity=result)
        refresh_token = create_refresh_token(identity=result)

        return generate_response({"access_token": access_token, "refresh_token": refresh_token},
                                 request)
