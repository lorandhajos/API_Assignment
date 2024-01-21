import json

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields
from sqlalchemy.sql import text

from .utils import decrypt, generate_response, get_db_engine

class WatchlistSchema(Schema):
    films = fields.List(fields.Dict())
    series = fields.List(fields.Dict())

class Watchlist(MethodView):
    @jwt_required(optional=False)
    def get(self, watchlist_id):
        """
        Watchlist
        ---
        description: Returns the watchlist
        security:
            - JWT: []
        parameters:
            - in: path
              name: watchlist_id
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
                                            {"watchlist_id": watchlist_id})

            if resultFilms.rowcount != 0:
                for film in resultFilms:
                    result[0].append(film._asdict())

            resultSeries = connection.execute(text(f"SELECT getWatchlistSeriesForID(:watchlist_id);"),
                                            {"watchlist_id": watchlist_id})

            if resultSeries.rowcount != 0:
                for series in resultSeries:
                    result[1].append(series._asdict())

            return generate_response({"films": result[0], "series": result[1]}, request)

class History(MethodView):
    @jwt_required(optional=False)
    def get(self, history_id):
        """
       History
        ---
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
