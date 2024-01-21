import json

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields
from sqlalchemy.sql import text

from .utils import decrypt, generate_response, get_db_engine

class ReportNamesSchema(Schema):
    title = fields.String(required=True)

class ReportViewsSchema(Schema):
    views = fields.Integer(required=True)

class ReportCountrySchema(Schema):
    country = fields.String(required=True)

class FilmNames(MethodView):
    @jwt_required(optional=False)
    def get(self):
        """
        Film Names Report
        ---
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
        """
        data = decrypt(json.loads(get_jwt_identity()))

        engine = get_db_engine(data)
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT getMovieNames();")).all()

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
        """
        data = decrypt(json.loads(get_jwt_identity()))

        engine = get_db_engine(data)
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT getMovieViews();")).all()

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
        """
        data = decrypt(json.loads(get_jwt_identity()))

        engine = get_db_engine(data)
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT getSeriesTitle();")).all()

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
        """
        data = decrypt(json.loads(get_jwt_identity()))

        engine = get_db_engine(data)
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT getSeriesViews();")).all()

        totalViews = []

        for view in result:
            totalViews.append({"views": view[0]})

        return generate_response(totalViews, request)

class Country(MethodView):
    def get(self):
        """
        Country Report
        ---
        description: This is the function which returns the total count of the countries
        security:
            - JWT: []
        responses:
            200:
                description: Total count of the countries returned
                content:
                    application/json:
                        schema: CountrySchema
                    application/xml:
                        schema: CountrySchema
        """
        engine = get_db_engine()
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT getProfileCountry()")).all()

        countryCount = [dict(row) for row in result]

        return generate_response(countryCount, request)
