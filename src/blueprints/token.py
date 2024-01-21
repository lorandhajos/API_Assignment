from flask import request
from flask.views import MethodView
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)
from marshmallow import Schema, fields

from .utils import generate_response

class RefreshResponseSchema(Schema):
    access_token = fields.String(required=True)

class Token(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh Token
        ---
        tags:
            - token
        description: Token refresh endpoint
        security:
            - JWT: []
        responses:
            200:
                description: Token refresh successful
                content:
                    application/json:
                        schema: RefreshResponseSchema
                    application/xml:
                        schema: RefreshResponseSchema
            401:
                description: Token refresh failed
                content:
                    application/json:
                        schema: ErrorResponseSchema
                    application/xml:
                        schema: ErrorResponseSchema
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user)

        return generate_response({"access_token": new_token}, request)
