import json

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields
from sqlalchemy.sql import text

from ..utils import decrypt, generate_response, get_db_engine

class SeriesSchema(Schema):
    id = fields.Integer(required=False)
    title = fields.String(required=True)
    views = fields.Integer(required=True)

class SeriesResponseSchema(Schema):
    title = fields.String(required=True)
    series_id = fields.Integer(required=True)

class Series(MethodView):
    @jwt_required(optional=False)
    def post(self):
        """
        Create series
        ---
        tags:
            - series
        description: Creates a new series
        security:
            - JWT: []
        requestBody:
            content:
                application/json:
                    schema: SeriesSchema
        responses:
            201:
                description: Series created
                content:
                    application/json:
                        schema: SeriesResponseSchema
                    application/xml:
                        schema: SeriesResponseSchema
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
            series_id = request.json.get('series_id')
            title = request.json.get('title')
            views = request.json.get('views')

            engine = get_db_engine(data)
            with engine.connect() as connection:
                result = connection.execute(text("CALL createSeriesElement(:series_id, :title, :views);"), {"id":id, "title":title, "views":views}).first()
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, 201)

    @jwt_required(optional=False)
    def get(self, id=None):
        """
        Get series
        ---
        tags:
            - series
        description: Get series
        security:
            - JWT: []
        responses:
            200:
                description: Series
                content:
                    application/json:
                        schema: SeriesResponseSchema
                    application/xml:
                        schema: SeriesResponseSchema
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
                    result = connection.execute(text("SELECT * FROM selectSeries;")).fetchall()
                else:
                    result = connection.execute(text("SELECT * FROM selectSeries WHERE series_id = :id;"), {"id": id}).first()
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, 200)

    @jwt_required(optional=False)
    def put(self, id):
        """
        Update series
        ---
        tags:
            - series
        description: Updates a series
        security:
            - JWT: []
        requestBody:
            content:
                application/json:
                    schema: SeriesSchema
        responses:
            200:
                description: Series updated
                content:
                    application/json:
                        schema: SeriesResponseSchema
                    application/xml:
                        schema: SeriesResponseSchema
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
            title = request.json.get('title')
            views = request.json.get('views')

            engine = get_db_engine(data)
            with engine.connect() as connection:
                result = connection.execute(text("CALL updateSeriesElement(:series_id, :title, :views);"), {"id":id, "title":title, "views":views}).first()
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, 200)

    @jwt_required(optional=False)
    def delete(self, id):
        """
        Delete series
        ---
        tags:
            - series
        description: Deletes a series
        security:
            - JWT: []
        responses:
            200:
                description: Series deleted
                content:
                    application/json:
                        schema: SeriesResponseSchema
                    application/xml:
                        schema: SeriesResponseSchema
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
                result = connection.execute(text("CALL deleteSeriesElement(:id);"), {"id": id}).first()
        except Exception:
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response(result, 200)
