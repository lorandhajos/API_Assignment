import json

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields
from sqlalchemy.sql import text

from ..utils import decrypt, generate_response, get_db_engine

class ProfileSchema(Schema):
    account_id = fields.Integer(required=True)
    profile_image = fields.String(required=True)
    profile_child = fields.Bool(required=True)
    age = fields.Integer(required=True)
    language = fields.String(required=True)
    watchlist_id = fields.Integer(required=True)
    history_id = fields.Integer(required=True)

class ProfileResponseSchema(Schema):
    account_id = fields.Integer(required=True)
    profile_image = fields.String(required=True)
    profile_child = fields.Bool(required=True)
    age = fields.Integer(required=True)
    language = fields.String(required=True)
    watchlist_id = fields.Integer(required=True)
    history_id = fields.Integer(required=True)
    profile_id = fields.Integer(required=True)

class Profile(MethodView):
    @jwt_required(optional=False)
    def post(self):
        """
        Profile
        ---
        tags:
            - profile
        description: Creates a new profile
        security:
            - JWT: []
        requestBody:
            content:
                application/json:
                    schema: ProfileSchema
        responses:
            201:
                description: Profile created
                content:
                    application/json:
                        schema: ProfileResponseSchema
                    application/xml:
                        schema: ProfileResponseSchema
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
            name = request.json.get('name')
            name = request.json.get('account_id')

            engine = get_db_engine(data)
            with engine.connect() as connection:
                connection.execute(text(f"SELECT createProfile(:name, :account_id);"),
                                            {"name": name, "account_id": account_id})
                connection.commit()
        except Exception as e:
            print(e)
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response({"msg": "Operation successful"}, request, 201)

    @jwt_required(optional=False)
    def get(self, id=None):
        """
        Profile(s)
        ---
        tags:
            - profile
        description: Returns the profile(s)
        security:
            - JWT: []
        responses:
            200:
                description: Profile(s) returned
                content:
                    application/json:
                        schema: ProfileSchema
                    application/xml:
                        schema: ProfileSchema
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
                    result = connection.execute(text(f"SELECT getProfilesForID(:account_id);"),
                                            {"account_id": id}).fetchall()
                else:
                    result = connection.execute(text(f"SELECT getProfilesForID(:account_id);"),
                                            {"account_id": id}).first()
        except Exception as e:
            print(e)
            return generate_response({"msg": "Bad request"}, request, 400)

        many = isinstance(result, list)
        schema = SeriesResponseSchema()
        result = schema.dump(result, many=many)

        return generate_response(result, request)

    @jwt_required(optional=False)
    def put(self, profile_id):
        """
        Profile
        ---
        tags:
            - profile
        description: Updates a profile
        security:
            - JWT: []
        parameters:
            - in: path
              name: profile_id
              schema:
                type: integer
              required: true
              description: The profile ID
        requestBody:
            content:
                application/json:
                    schema: ProfileSchema
        responses:
            200:
                description: Profile updated
                content:
                    application/json:
                        schema: ProfileResponseSchema
                    application/xml:
                        schema: ProfileResponseSchema
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
            name = request.json.get('name')

            engine = get_db_engine(data)
            with engine.connect() as connection:
                connection.execute(text(f"SELECT updateProfile(:name, :profile_id);"),
                                            {"name": name, "profile_id": profile_id})
                connection.commit()
        except Exception as e:
            print(e)
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response({"msg": "Operation successful"}, request)

    @jwt_required(optional=False)
    def delete(self, profile_id):
        """
        Profile
        ---
        tags:
            - profile
        description: Deletes a profile
        security:
            - JWT: []
        parameters:
            - in: path
              name: profile_id
              schema:
                type: integer
              required: true
              description: The profile ID
        responses:
            200:
                description: Profile deleted
                content:
                    application/json:
                        schema: ProfileResponseSchema
                    application/xml:
                        schema: ProfileResponseSchema
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
                connection.execute(text(f"SELECT deleteProfile(:profile_id);"),
                                            {"profile_id": profile_id})
                connection.commit()
        except Exception as e:
            print(e)
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response({"msg": "Operation successful"}, request)
