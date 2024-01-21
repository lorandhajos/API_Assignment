import requests
import os
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
        responses:
            200:
                description: Random text
                content:
                    application/json:
                        schema: RandomSchema
                    application/xml:
                        schema: RandomSchema
            400:
                description: Bad request
                content:
                    application/json:
                        schema: ErrorResponseSchema
                    application/xml:
                        schema: ErrorResponseSchema
        """
        number = request.args.get('number')

        headers = {
            'X-Api-Key': os.environ.get('RANDOM_API_KEY'),
            'Accept': 'application/json'
        }

        result = requests.get(f"https://randommer.io/api/Text/LoremIpsum?loremType=business&type=paragraphs&number={number}",
                              headers=headers).json()

        return generate_response(result, request)
