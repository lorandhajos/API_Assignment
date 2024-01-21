import json

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields
from sqlalchemy.sql import text

from ..utils import decrypt, generate_response, get_db_engine

class HistorySchema(Schema):
    history_id = fields.Integer(required=True)
    movie_id = fields.Integer(required=True)

class HistoryResponseSchema(Schema):
    history_id = fields.Integer(required=True)
    movie_id = fields.Integer(required=True)
    history_movies_id = fields.Integer(required=True)

class History(MethodView):
    @jwt_required(optional=False)
    def post(self):
        """
        Create history
        ---
        tags:
            - history
        description: Creates a new history
        security:
            - JWT: []
        requestBody:
            content:
                application/json:
                    schema: HistorySchema
        responses:
            201:
                description: History created
                content:
                    application/json:
                        schema: HistoryResponseSchema
                    application/xml:
                        schema: HistoryResponseSchema
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
    def get(self, history_id=None):
        """
        History
        ---
        tags:
            - history
        description: Returns full history in the same format as the watchlist function
        security:
            - JWT: []
        parameters:
            - in: path
              name: history_id
              schema:
                type: integer
              required: true
              description: The history ID
        responses:
            200:
                description: History returned
                content:
                    application/json:
                        schema: WatchlistSchema
                    application/xml:
                        schema: WatchlistSchema
        """
        data = decrypt(json.loads(get_jwt_identity()))

        engine = get_db_engine(data)
        with engine.connect() as connection:
            result = [[], []]

            resultFilms = connection.execute(text(f"SELECT getHistoryMoviesForID(:history_id);"),
                                            {"history_id": history_id})

            if resultFilms.rowcount != 0:
                for film in resultFilms:
                    result[0].append(film._asdict())

            resultSeries = connection.execute(text(f"SELECT getHistorySeriesForID(:history_id);"),
                                                {"history_id": history_id})

            if resultSeries.rowcount != 0:
                for series in resultSeries:
                    result[1].append(series._asdict())

            return generate_response({"films": result[0], "series": result[1]}, request)

    @jwt_required(optional=False)
    def put(self):
        """
        Update history
        ---
        tags:
            - history
        description: Updates a history
        security:
            - JWT: []
        requestBody:
            content:
                application/json:
                    schema: HistorySchema
        responses:
            200:
                description: History updated
                content:
                    application/json:
                        schema: HistoryResponseSchema
                    application/xml:
                        schema: HistoryResponseSchema
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
    def delete(self):
        """
        Delete history
        ---
        tags:
            - history
        description: Deletes a history
        security:
            - JWT: []
        responses:
            200:
                description: History deleted
                content:
                    application/json:
                        schema: HistoryResponseSchema
                    application/xml:
                        schema: HistoryResponseSchema
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
