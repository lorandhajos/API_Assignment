import json

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields
from sqlalchemy.sql import text

from ..utils import decrypt, generate_response, get_db_engine

class AccountSchema(Schema):
    account_id = fields.Integer(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    payment_method = fields.String(required=True)
    blocked = fields.Boolean(required=True)
    login_attempts = fields.Integer(required=True)
    last_login = fields.Date(required=True)
    subscription_id = fields.Integer(required=True)

class Account(MethodView):
    @jwt_required(optional=False)
    def post(self):
        """
        Create a new account
        ---
        tags:
          - account
        description: Create a new account
        security:
          - JWT: []
        requestBody:
            content:
                application/json:
                    schema: AccountSchema
        responses:
            201:
                description: Account created
                content:
                    application/json:
                        schema: AccountSchema
                    application/xml:
                        schema: AccountSchema
            400:
                description: Bad request
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
            data = decrypt(json.loads(get_jwt_identity()))
        except Exception:
            return generate_response({"msg": "Bad username or password"}, request, 401)

        try:
            id = request.json.get('id')
            email = request.json.get('email')
            password = request.json.get('password')
            payment_method = request.json.get('payment_method')
            blocked = request.json.get('blocked')
            login_attempts = request.json.get('login_attempts')
            last_login = request.json.get('last_login')
            subscription_id = request.json.get('subscription_id')

            engine = get_db_engine(data)
            with engine.connect() as connection:
                result = connection.execute(text("""CALL createAccountElement(:id, :email, :password,
                                                 :payment_method, :blocked, :login_attempts, :last_login,
                                                 :subscription_id);"""),
                                            {"id": id, "email": email, "password": password,
                                             "payment_method": payment_method, "blocked": blocked,
                                             "login_attempts": login_attempts, "last_login": last_login,
                                             "subscription_id": subscription_id}).first()
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, request, 201)

    @jwt_required(optional=False)
    def get(self, id=None):
        """
        Get account(s)
        ---
        tags:
          - account
        description: Get account(s)
        security:
          - JWT: []
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              required: false
              description: Account ID
        responses:
            200:
                description: Account(s)
                content:
                    application/json:
                        schema: AccountSchema
                    application/xml:
                        schema: AccountSchema
            400:
                description: Bad request
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
            data = decrypt(json.loads(get_jwt_identity()))
        except Exception:
            return generate_response({"msg": "Bad username or password"}, request, 401)

        try:
            engine = get_db_engine(data)
            with engine.connect() as connection:
                if id is None:
                    result = connection.execute(text("SELECT * FROM selectaccount;")).fetchall()
                else:
                    result = connection.execute(text("SELECT * FROM selectaccount WHERE account_id=:id"),
                                                {"id": id}).first()
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        schema = AccountSchema()
        result = schema.dump(result, many=True)

        return generate_response(result, request)

    @jwt_required(optional=False)
    def put(self, id):
        """
        Update account
        ---
        tags:
          - account
        description: Update account
        security:
          - JWT: []
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              required: true
              description: Account ID
        requestBody:
            content:
                application/json:
                    schema: AccountSchema
        responses:
            200:
                description: Account updated
                content:
                    application/json:
                        schema: AccountSchema
                    application/xml:
                        schema: AccountSchema
            400:
                description: Bad request
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
            data = decrypt(json.loads(get_jwt_identity()))
        except Exception:
            return generate_response({"msg": "Bad username or password"}, request, 401)

        try:
            email = request.json.get('email')
            password = request.json.get('password')
            payment_method = request.json.get('payment_method')
            blocked = request.json.get('blocked')
            login_attempts = request.json.get('login_attempts')
            last_login = request.json.get('last_login')
            subscription_id = request.json.get('subscription_id')

            engine = get_db_engine(data)
            with engine.connect() as connection:
                result = connection.execute(text("""CALL updateAccountElement(:id, :email, :password,
                                                 :payment_method, :blocked, :login_attempts, :last_login,
                                                 :subscription_id);"""),
                                            {"id": id, "email": email, "password": password,
                                             "payment_method": payment_method, "blocked": blocked,
                                             "login_attempts": login_attempts, "last_login": last_login,
                                             "subscription_id": subscription_id}).first()
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, request)

    @jwt_required(optional=False)
    def delete(self, id):
        """
        Delete account
        ---
        tags:
          - account
        description: Delete account
        security:
            - JWT: []
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              required: true
              description: Account ID
        responses:
            200:
                description: Account deleted
                content:
                    application/json:
                        schema: AccountSchema
                    application/xml:
                        schema: AccountSchema
            400:
                description: Bad request
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
            data = decrypt(json.loads(get_jwt_identity()))
        except Exception:
            return generate_response({"msg": "Bad username or password"}, request, 401)

        try:
            engine = get_db_engine(data)
            with engine.connect() as connection:
                result = connection.execute(text("CALL deleteAccountElement(:id)"), {"id": id}).first()
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, request)
