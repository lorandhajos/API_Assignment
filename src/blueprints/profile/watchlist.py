import json

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields
from sqlalchemy.sql import text

from ..utils import decrypt, generate_response, get_db_engine

class WatchlistSchema(Schema):
    films = fields.List(fields.Dict())
    series = fields.List(fields.Dict())

class WatchlistResponseSchema(Schema):
    watchlist_id = fields.Integer(required=True)
    films = fields.List(fields.Dict())
    series = fields.List(fields.Dict())

class Watchlist(MethodView):
    @jwt_required(optional=False)
    def post(self):
        """
        Create watchlist
        ---
        tags:
            - watchlist
        description: Creates a new watchlist
        security:
            - JWT: []
        requestBody:
            content:
                application/json:
                    schema: WatchlistSchema
        responses:
            201:
                description: Watchlist created
                content:
                    application/json:
                        schema: WatchlistResponseSchema
                    application/xml:
                        schema: WatchlistResponseSchema
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
        Watchlist
        ---
        tags:
            - watchlist
        description: Returns the watchlist
        security:
            - JWT: []
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              required: true
              description: The watchlist ID
        responses:
            200:
                description: Watchlist returned
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

            resultFilms = connection.execute(text(f"SELECT getWatchlistFilmsForID(:watchlist_id);"),
                                            {"watchlist_id": id})

            if resultFilms.rowcount != 0:
                for film in resultFilms:
                    result[0].append(film._asdict())

            resultSeries = connection.execute(text(f"SELECT getWatchlistSeriesForID(:watchlist_id);"),
                                            {"watchlist_id": id})

            if resultSeries.rowcount != 0:
                for series in resultSeries:
                    result[1].append(series._asdict())

            return generate_response({"films": result[0], "series": result[1]}, request)

    @jwt_required(optional=False)
    def put(self, id):
        """
        Update watchlist
        ---
        tags:
            - watchlist
        description: Updates a watchlist
        security:
            - JWT: []
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              required: true
              description: The watchlist ID
        requestBody:
            content:
                application/json:
                    schema: WatchlistSchema
        responses:
            200:
                description: Watchlist updated
                content:
                    application/json:
                        schema: WatchlistResponseSchema
                    application/xml:
                        schema: WatchlistResponseSchema
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
        Delete watchlist
        ---
        tags:
            - watchlist
        description: Deletes a watchlist
        security:
            - JWT: []
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              required: true
              description: The watchlist ID
        responses:
            200:
                description: Watchlist deleted
                content:
                    application/json:
                        schema: WatchlistResponseSchema
                    application/xml:
                        schema: WatchlistResponseSchema
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
        pass
