import json

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields
from sqlalchemy.sql import text

from ..utils import decrypt, generate_response, get_db_engine

class InterestSchema(Schema):
    profile_id = fields.Integer(required=True)
    genre_id = fields.Integer(required=True)

class Interests(MethodView):
    @jwt_required(optional=False)
    def post(self):
        """
        Create interest
        ---
        tags:
            - interest
        description: Creates a new interest
        security:
            - JWT: []
        requestBody:
            content:
                application/json:
                    schema: InterestSchema
        responses:
            201:
                description: Interest created
                content:
                    application/json:
                        schema: InterestSchema
                    application/xml:
                        schema: InterestSchema
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
            profile_id = request.json.get('profile_id')
            genre_id = request.json.get('genre_id')

            engine = get_db_engine(data)
            with engine.connect() as connection:
                result = connection.execute(text("CALL createInterestElement(:profile_id, :genre_id);"), {"profile_id": profile_id, "genre_id": genre_id}).first()
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, request, 201)

    @jwt_required(optional=False)
    def get(self, id=None):
        """
        Get interest(s)
        ---
        tags:
            - interest
        description: Get interest(s)
        security:
            - JWT: []
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              required: false
              description: The interest ID
        responses:
            200:
                description: Interest(s)
                content:
                    application/json:
                        schema: InterestSchema
                    application/xml:
                        schema: InterestSchema
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
                    result = connection.execute(text("SELECT * FROM selectInterests;")).fetchall()
                else:
                    result = connection.execute(text("SELECT * FROM selectInterests WHERE profile_id = :id;"), {"id": id}).first()
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, request)

    @jwt_required(optional=False)
    def put(self, id):
        """
        Update interest
        ---
        tags:
            - interest
        description: Updates an interest
        security:
            - JWT: []
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              required: true
              description: The interest ID
        requestBody:
            content:
                application/json:
                    schema: InterestSchema
        responses:
            200:
                description: Interest updated
                content:
                    application/json:
                        schema: InterestSchema
                    application/xml:
                        schema: InterestSchema
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
            genre_id = request.json.get('genre_id')
            desired_genre_id = request.json.get('desired_genre_id')

            engine = get_db_engine(data)
            with engine.connect() as connection:
                result = connection.execute(text("CALL updateInterestElement(:profile_id, :genre_id, :desired_genre_id);"), {"profile_id": id, "genre_id": genre_id, "desired_genre_id": desired_genre_id})
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, request, 201)

    @jwt_required(optional=False)
    def delete(self, id):
        """
        Delete interest
        ---
        tags:
            - interest
        description: Deletes an interest
        security:
            - JWT: []
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              required: true
              description: The interest ID
        responses:
            200:
                description: Interest deleted
                content:
                    application/json:
                        schema: InterestSchema
                    application/xml:
                        schema: InterestSchema
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
                result = connection.execute(text("CALL deleteInterestElement(:id);"), {"id": id}).first()
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, request)
