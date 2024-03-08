import json

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields
from sqlalchemy.sql import text

from ..utils import decrypt, generate_response, get_db_engine

class PreferencesSchema(Schema):
    name = fields.String(required=True)

class PreferencesResponseSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)

class Preferences(MethodView):
    @jwt_required(optional=False)
    def post(self):
        """
        Add a new preference
        ---
        tags:
            - preferences
        description: Add a new preference
        security:
            - JWT: []
        requestBody:
            content:
                application/json:
                    schema: PreferencesSchema
        responses:
            201:
                description: Preference added
                content:
                    application/json:
                        schema: PreferencesResponseSchema
                    application/xml:
                        schema: PreferencesResponseSchema
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
                result = connection.execute(text(f"SELECT addPreference({data['id']}, '{request.json['name']}');")).all()
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, request, 201)

    @jwt_required(optional=False)
    def get(self, id=None):
        """
        Get all preferences
        ---
        tags:
            - preferences
        description: Get all preferences
        security:
            - JWT: []
        responses:
            200:
                description: Preferences returned
                content:
                    application/json:
                        schema: PreferencesSchema
                    application/xml:
                        schema: PreferencesSchema
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
                    result = connection.execute(text(f"SELECT * FROM getPreferences({data['id']});")).all()
                else:
                    result = connection.execute(text(f"SELECT * FROM getPreference({data['id']}, {id});")).all()
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, request)

    @jwt_required(optional=False)
    def put(self, id):
        """
        Update a preference
        ---
        tags:
            - preferences
        description: Update a preference
        security:
            - JWT: []
        requestBody:
            content:
                application/json:
                    schema: PreferencesSchema
        responses:
            200:
                description: Preference updated
                content:
                    application/json:
                        schema: PreferencesSchema
                    application/xml:
                        schema: PreferencesSchema
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
                result = connection.execute(text(f"SELECT updatePreference({data['id']}, {id}, '{request.json['name']}');")).all()
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, request, 201)

    @jwt_required(optional=False)
    def delete(self, id):
        """
        Delete a preference
        ---
        tags:
            - preferences
        description: Delete a preference
        security:
            - JWT: []
        responses:
            200:
                description: Preference deleted
                content:
                    application/json:
                        schema: PreferencesSchema
                    application/xml:
                        schema: PreferencesSchema
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
                result = connection.execute(text(f"SELECT deletePreference({data['id']}, {id});")).all()
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, request)
