import json

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields
from sqlalchemy.sql import text

from .utils import decrypt, generate_response, get_db_engine

class AccessSchema(Schema):
    access = fields.Boolean(required=True)

class AccessFilms(MethodView):
    @jwt_required(optional=False)
    def get(self, profile_id, film_id):
        """
        Access Films
        ---
        description: These 2 functions grant or deny access to the film or series, depending on the profile age and films restriction
        security:
            - JWT: []
        parameters:
            - in: path
              name: profile_id
              schema:
                type: integer
              required: true
              description: The user ID
            - in: path
              name: film_id
              schema:
                type: integer
              required: true
              description: The film ID
        responses:
            200:
                description: Access granted
                content:
                    application/json:
                        schema: AccessSchema
                    application/xml:
                        schema: AccessSchema
            401:
                description: Access denied
                content:
                    application/json:
                        schema: AccessSchema
                    application/xml:
                        schema: AccessSchema
        """
        data = decrypt(json.loads(get_jwt_identity()))

        engine = get_db_engine(data)
        with engine.connect() as connection:
            current_age = connection.execute(text(f"SELECT getAgeProfile(:profile_id);"),
                                                {"profile_id": profile_id}).first()[0]

            film_age = connection.execute(text(f"SELECT getAgeRestrictorFilms(:film_id)"),
                                        {"film_id": film_id}).first()[0]

            return generate_response({"access": film_age <= current_age}, request)

class AccessSeries(MethodView):
    @jwt_required(optional=False)
    def get(self, profile_id, series_id):
        """
        Access Series
        ---
        description: These 2 functions grant or deny access to the film or series, depending on the profile age and films restriction
        security:
            - JWT: []
        parameters:
            - in: path
              name: profile_id
              schema:
                type: integer
              required: true
              description: The user ID
            - in: path
              name: series_id
              schema:
                type: integer
              required: true
              description: The series ID
        responses:
            200:
                description: Access granted
                content:
                    application/json:
                        schema: AccessSchema
                    application/xml:
                        schema: AccessSchema
            401:
                description: Access denied
                content:
                    application/json:
                        schema: AccessSchema
                    application/xml:
                        schema: AccessSchema
        """
        data = decrypt(json.loads(get_jwt_identity()))

        engine = get_db_engine(data)
        with engine.connect() as connection:
            current_age = connection.execute(text(f"SELECT getAgeProfile(:profile_id)"),
                                            {"profile_id": profile_id}).first()[0]

            series_age = connection.execute(text(f"SELECT getAgeRestrictorSeries(:series_id);"),
                                            {"series_id": series_id}).first()[0]

            return generate_response({"access": series_age <= current_age}, request)
