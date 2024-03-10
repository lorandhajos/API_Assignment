import requests
from flask import request
from flask.views import MethodView

from .utils import generate_response

class Random(MethodView):
    def get(self):
        """
        Get loren ipsum
        ---
        tags:
            - random
        description: Get loren ipsum
        parameters:
            - in: query
              name: number
              schema:
                type: integer
              required: true
              description: Number of paragraphs
            - in: header
              name: X-Api-Key
              schema:
                type: string
              required: true
              description: API key
        responses:
            200:
                description: Random text
                content:
                    application/json:
                        schema: text
                    application/xml:
                        schema: text
            400:
                description: Bad request
                content:
                    application/json:
                        schema: ErrorResponseSchema
                    application/xml:
                        schema: ErrorResponseSchema
            401:
                description: Unauthorized
                content:
                    application/json:
                        schema: ErrorResponseSchema
                    application/xml:
                        schema: ErrorResponseSchema
        """
        number = request.args.get('number')
        api_key = request.headers.get('X-Api-Key')

        headers = {
            'X-Api-Key': api_key,
            'Accept': 'application/json'
        }

        result = requests.get(f"https://randommer.io/api/Text/LoremIpsum?loremType=business&type=paragraphs&number={number}",
                              headers=headers).json()

        if result and 'status' in result and result['status'] != 200:
            return generate_response({"msg": result['title']}, request, result['status'])

        return generate_response(result, request)
