import json

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields
from sqlalchemy.sql import text

from ..utils import decrypt, generate_response, get_db_engine

class MovieSchema(Schema):
    title = fields.String(required=True)
    duration = fields.String(required=True)

class MovieResponseSchema(Schema):
    title = fields.String(required=True)
    duration = fields.String(required=True)
    movie_id = fields.Integer(required=True)

class Movies(MethodView):
    @jwt_required(optional=False)
    def post(self):
        """
        Create movie
        ---
        tags:
            - movie
        description: Creates a new movie
        security:
            - JWT: []
        requestBody:
            content:
                application/json:
                    schema: MovieSchema
        responses:
            201:
                description: Movie created
                content:
                    application/json:
                        schema: MovieResponseSchema
                    application/xml:
                        schema: MovieResponseSchema
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
    def get(self, id=None):
        """
        Get movie(s)
        ---
        tags:
            - movie
        description: Get movie(s)
        security:
            - JWT: []
        responses:
            200:
                description: Movie(s)
                content:
                    application/json:
                        schema: MovieResponseSchema
                    application/xml:
                        schema: MovieResponseSchema
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
        Update movie
        ---
        tags:
            - movie
        description: Update movie
        security:
            - JWT: []
        requestBody:
            content:
                application/json:
                    schema: MovieSchema
        responses:
            200:
                description: Movie updated
                content:
                    application/json:
                        schema: MovieResponseSchema
                    application/xml:
                        schema: MovieResponseSchema
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
    def delete(self):
        """
        Delete movie
        ---
        tags:
            - movie
        description: Delete movie
        security:
            - JWT: []
        responses:
            200:
                description: Movie deleted
                content:
                    application/json:
                        schema: MovieResponseSchema
                    application/xml:
                        schema: MovieResponseSchema
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
