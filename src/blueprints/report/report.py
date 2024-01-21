import json

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields
from sqlalchemy.sql import text

from ..utils import decrypt, generate_response, get_db_engine

class ReportNamesSchema(Schema):
    title = fields.String(required=True)

class ReportViewsSchema(Schema):
    views = fields.Integer(required=True)

class ReportCountrySchema(Schema):
    number = fields.String(required=True)

class FilmNames(MethodView):
    @jwt_required(optional=False)
    def get(self):
        """
        Film Names Report
        ---
        tags:
            - report
        description: This function returns a total view count with the name
        security:
            - JWT: []
        responses:
            200:
                description: Total view count returned
                content:
                    application/json:
                        schema: ReportNamesSchema
                    application/xml:
                        schema: ReportNamesSchema
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
            return generate_response({"error": "Bad username or password"}, request, 401)

        try:
            engine = get_db_engine(data)
            with engine.connect() as connection:
                result = connection.execute(text("SELECT getMovieNames();")).all()
        except Exception:
            return generate_response({"error": "Bad request"}, request, 400)

        totalNames = []

        for name in result:
            totalNames.append({"title": name[0]})

        return generate_response(totalNames, request)

class FilmViews(MethodView):
    @jwt_required(optional=False)
    def get(self):
        """
        Film Views Report
        ---
        tags:
            - report
        description: Thesis function returns a total view count with the name
        security:
            - JWT: []
        responses:
            200:
                description: Total view count returned
                content:
                    application/json:
                        schema: ReportViewsSchema
                    application/xml:
                        schema: ReportViewsSchema
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
            return generate_response({"error": "Bad username or password"}, request, 401)

        try:
            engine = get_db_engine(data)
            with engine.connect() as connection:
                result = connection.execute(text("SELECT getMovieViews();")).all()
        except Exception:
            return generate_response({"error": "Bad request"}, request, 400)

        totalViews = []

        for view in result:
            totalViews.append({"views": view[0]})

        return generate_response(totalViews, request)

class SeriesNames(MethodView):
    @jwt_required(optional=False)
    def get(self):
        """
        Series Names Report
        ---
        tags:
            - report
        description: These 2 functions fetch a total view count with the name
        security:
            - JWT: []
        responses:
            200:
                description: Total view count returned
                content:
                    application/json:
                        schema: ReportNamesSchema
                    application/xml:
                        schema: ReportNamesSchema
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
            return generate_response({"error": "Bad username or password"}, request, 401)

        try:
            engine = get_db_engine(data)
            with engine.connect() as connection:
                result = connection.execute(text("SELECT getSeriesTitle();")).all()
        except Exception:
            return generate_response({"error": "Bad request"}, request, 400)

        totalNames = []

        for name in result:
            totalNames.append({"title": name[0]})

        return generate_response(totalNames, request)

class SeriesViews(MethodView):
    @jwt_required(optional=False)
    def get(self):
        """
        Series Views Report
        ---
        tags:
            - report
        description: These 2 functions fetch a total view count with the name
        security:
            - JWT: []
        responses:
            200:
                description: Total view count returned
                content:
                    application/json:
                        schema: ReportViewsSchema
                    application/xml:
                        schema: ReportViewsSchema
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
            return generate_response({"error": "Bad username or password"}, request, 401)

        try:
            engine = get_db_engine(data)
            with engine.connect() as connection:
                result = connection.execute(text("SELECT getSeriesViews();")).all()
        except Exception:
            return generate_response({"error": "Bad request"}, request, 400)

        totalViews = []

        for view in result:
            totalViews.append({"views": view[0]})

        return generate_response(totalViews, request)

class Country(MethodView):
    @jwt_required(optional=False)
    def get(self):
        """
        Country Report
        ---
        tags:
            - report
        description: This is the function which returns the total count of the countries
        security:
            - JWT: []
        responses:
            200:
                description: Total count of the countries returned
                content:
                    application/json:
                        schema: ReportCountrySchema
                    application/xml:
                        schema: ReportCountrySchema
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
            return generate_response({"error": "Bad username or password"}, request, 401)

        try:
            engine = get_db_engine(data)
            with engine.connect() as connection:
                result = connection.execute(text("SELECT getNOfUsersPerCountry()")).all()
        except Exception:
            return generate_response({"error": "Bad request"}, request, 400)

        totalNumberOfUsers = []

        for number in result:
            totalNumberOfUsers.append({"number" : number[0]})

        return generate_response(totalNumberOfUsers, request)
