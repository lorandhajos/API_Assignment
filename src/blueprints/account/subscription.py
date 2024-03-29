import json

from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import Schema, fields
from sqlalchemy.sql import text

from ..utils import decrypt, generate_response, get_db_engine

class SubscriptionSchema(Schema):
    description = fields.String(required=True)
    subscription_price = fields.Float(required=True)

class SubscriptionResponseSchema(Schema):
    description = fields.String(required=True)
    subscription_price = fields.Float(required=True)
    subscription_id = fields.Integer(required=True)

class Subscription(MethodView):
    @jwt_required(optional=False)
    def post(self):
        """
        Create subscription
        ---
        tags:
            - subscription
        description: Creates a new subscription
        security:
            - JWT: []
        requestBody:
            content:
                application/json:
                    schema: SubscriptionSchema
        responses:
            201:
                description: Subscription created
                content:
                    application/json:
                        schema: ErrorResponseSchema
                    application/xml:
                        schema: ErrorResponseSchema
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
            description = request.json.get('description')
            subscription_price = request.json.get('subscription_price')

            engine = get_db_engine(data)
            with engine.connect() as connection:
                connection.execute(text("CALL createSubscriptionElement(:description, :subscription_price);"),
                                            {"description": description, "subscription_price": subscription_price})
                connection.commit()
        except Exception as e:
            print(e)
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response({"msg": "Operation successful"}, request, 201)

    @jwt_required(optional=False)
    def get(self, id=None):
        """
        Get subscription
        ---
        tags:
            - subscription
        description: Get subscription
        security:
            - JWT: []
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              required: false
              description: Subscription ID
        responses:
            200:
                description: Subscription
                content:
                    application/json:
                        schema: SubscriptionResponseSchema
                    application/xml:
                        schema: SubscriptionResponseSchema
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
                    result = connection.execute(text("SELECT * FROM selectSubscription")).all()
                else:
                    result = connection.execute(text("SELECT * FROM selectSubscription WHERE subscription_id=:id"),
                                                {"id": id}).first()
        except Exception as e:
            print(e)
            return generate_response({"msg": "Bad request"}, request, 400)

        many = isinstance(result, list)
        schema = SubscriptionResponseSchema()
        result = schema.dump(result, many=True)

        return generate_response(result, request)

    @jwt_required(optional=False)
    def put(self, id):
        """
        Update subscription
        ---
        tags:
            - subscription
        description: Updates a subscription
        security:
            - JWT: []
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              required: true
              description: Subscription ID
        requestBody:
            content:
                application/json:
                    schema: SubscriptionSchema
        responses:
            200:
                description: Subscription updated
                content:
                    application/json:
                        schema: ErrorResponseSchema
                    application/xml:
                        schema: ErrorResponseSchema
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
            description = request.json.get('description')
            subscription_price = request.json.get('subscription_price')

            engine = get_db_engine(data)
            with engine.connect() as connection:
                connection.execute(text("CALL updateSubscriptionElement(:id, :description, :subscription_price);"),
                                   {"id": id, "description": description, "subscription_price": subscription_price})
        except Exception as e:
            print(e)
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response({"msg": "Operation successful"}, request)

    @jwt_required(optional=False)
    def delete(self, id):
        """
        Delete subscription
        ---
        tags:
            - subscription
        description: Deletes a subscription
        security:
            - JWT: []
        parameters:
            - in: path
              name: id
              schema:
                type: integer
              required: true
              description: Subscription ID
        responses:
            200:
                description: Subscription deleted
                content:
                    application/json:
                        schema: ErrorResponseSchema
                    application/xml:
                        schema: ErrorResponseSchema
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
                connection.execute(text("CALL deleteSubscriptionElement(:id);"), {"id": id})
                connection.commit()
        except Exception as e:
            print(e)
            return generate_response({"msg": "Bad request"}, request, 400)

        return generate_response({"msg": "Operation successful"}, request)
