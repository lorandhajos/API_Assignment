import json

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields
from sqlalchemy.sql import text

from ..utils import decrypt, generate_response, get_db_engine

class GenreSchema(Schema):
    name = fields.String(required=True)
    age_restriction = fields.String(required=True)

class GenreResponseSchema(Schema):
    name = fields.String(required=True)
    age_restriction = fields.String(required=True)
    genre_id = fields.Integer(required=True)

class Genre(MethodView):
    @jwt_required(optional=False)
    def post(self):
        """
        Create genre
        ---
        tags:
            - genre
        description: Creates a new genre
        security:
            - JWT: []
        requestBody:
            content:
                application/json:
                    schema: GenreSchema
        responses:
            201:
                description: Genre created
                content:
                    application/json:
                        schema: GenreResponseSchema
                    application/xml:
                        schema: GenreResponseSchema
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
                result = connection.execute(text(""))
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, 201)

    @jwt_required(optional=False)
    def get(self, id=None):
        """
        Get genre(s)
        ---
        tags:
            - genre
        description: Get genre(s)
        security:
            - JWT: []
        responses:
            200:
                description: Genre(s)
                content:
                    application/json:
                        schema: GenreResponseSchema
                    application/xml:
                        schema: GenreResponseSchema
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
                result = connection.execute(text(""))
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, 201)

    @jwt_required(optional=False)
    def put(self):
        """
        Update genre
        ---
        tags:
            - genre
        description: Update genre
        security:
            - JWT: []
        requestBody:
            content:
                application/json:
                    schema: GenreSchema
        responses:
            200:
                description: Genre updated
                content:
                    application/json:
                        schema: GenreResponseSchema
                    application/xml:
                        schema: GenreResponseSchema
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
                        schema: ErrorResponseSchema"""
        try:
            data = decrypt(json.loads(get_jwt_identity()))
        except Exception:
            return generate_response({"msg": "Bad username or password"}, request, 401)

        try:
            engine = get_db_engine(data)
            with engine.connect() as connection:
                result = connection.execute(text(""))
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, 201)

    @jwt_required(optional=False)
    def delete(self, id):
        """
        Delete genre
        ---
        tags:
            - genre
        description: Delete genre
        security:
            - JWT: []
        responses:
            200:
                description: Genre deleted
                content:
                    application/json:
                        schema: GenreResponseSchema
                    application/xml:
                        schema: GenreResponseSchema
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
                        schema: ErrorResponseSchema"""
        try:
            data = decrypt(json.loads(get_jwt_identity()))
        except Exception:
            return generate_response({"msg": "Bad username or password"}, request, 401)

        try:
            engine = get_db_engine(data)
            with engine.connect() as connection:
                result = connection.execute(text(""))
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, 201)