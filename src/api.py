from datetime import timedelta

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from dotenv import dotenv_values
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, get_jwt_identity,
                                jwt_required)
from marshmallow import Schema, fields
from sqlalchemy import create_engine, text

config = dotenv_values("../.env")

spec = APISpec(
    title = "Netflix API",
    version = f"{config['API_VERSION']}.0.0",
    openapi_version = "3.1.0",
    plugins = [FlaskPlugin(), MarshmallowPlugin()],
    info = dict(
        description="Netflix API",
    ),
    servers = [dict(url=f"http://localhost:5000/api/{config['API_VERSION']}")],
    externalDocs = dict(
        description="GitHub",
        url="https://github.com/lorandhajos/API_Assignment",
    ),
)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class LoginResponseSchema(Schema):
    access_token = fields.String(required=True)
    refresh_token = fields.String(required=True)

class ErrorResponseSchema(Schema):
    msg = fields.String(required=True)

api_key_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
spec.components.security_scheme("JWT", api_key_scheme)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config['JWT_SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

CORS(app)

jwt = JWTManager(app)

sessions = {}

def get_db_engine(user, password):
    return create_engine(f"postgresql+psycopg://{user}:{password}@localhost:5432/{config['DB_NAME']}", echo=True)

@app.route('/docs')
def docs():
    """
    Swagger UI endpoint
    """
    return render_template('index.html', url=request.base_url.replace('/docs', '/openapi.json'))

@app.route('/openapi.json', methods=['GET'])
def openapi():
    """
    Swagger JSON endpoint
    """
    return jsonify(spec.to_dict())

@app.route('/login', methods=['POST'])
def login():
    """
    Login endpoint
    ---
    post:
        description: Login endpoint
        requestBody:
            content:
                application/json:
                    schema: LoginSchema
        responses:
            200:
                description: Login successful
                content:
                    application/json:
                        schema: LoginResponseSchema
            401:
                description: Bad username or password
                content:
                    application/json:
                        schema: ErrorResponseSchema
    """
    print(request.json)
    engine = get_db_engine(config['DB_USER'], config['DB_PASS'])
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT login(:email, :password)"),
                                    {"email": request.json.get('email'), "password": request.json.get('password')})
        if result.rowcount == 0:
            return jsonify({"msg": "Bad username or password"}), 401

        user_id = result.first()._asdict().get('id')
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)

        #sessions[user_id] = get_db_engine(request.json.get('email'), request.json.get('password'))

        return jsonify(access_token=access_token, refresh_token=refresh_token)

@app.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Token refresh endpoint
    """
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)

    return jsonify(access_token=new_token)

@app.route('/watchlist/<int:watchlist_id>/', methods=['GET'])
@jwt_required
def watchlist(watchlist_id):
    """
    Returns the watchlist
    """
    user_id = get_jwt_identity()
    with sessions[user_id].connect() as connection:
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

        return jsonify(result)

@app.route('/history/<int:history_id>', endpoint='history', methods=['GET'])
@jwt_required
def history(history):
    """
    Returns full history in the same format as the watchlist function
    """
    user_id = get_jwt_identity()
    with sessions[user_id].connect() as connection:
        result = [[], []]

        resultFilms = connection.execute(text(f"SELECT getHistoryMoviesForID(:history_id);"),
                                         {"history_id": history})

        if resultFilms.rowcount != 0:
            for film in resultFilms:
                result[0].append(film._asdict())

        resultSeries = connection.execute(text(f"SELECT getHistorySeriesForID(:history_id);"),
                                            {"history_id": history})

        if resultSeries.rowcount != 0:
            for series in resultSeries:
                result[1].append(series._asdict())

        return jsonify(result)

@app.route('/access_films/<int:film_id>', endpoint='access_films', methods=['GET'])
@jwt_required
def access(film_id):
    user_id = get_jwt_identity()
    with sessions[user_id].connect() as connection:
        profile_id = get_jwt_identity()

        curent_age = connection.execute(text(f"SELECT getAgeProfile(:profile_id);"),
                                        {"profile_id": profile_id})

        film_age = connection.execute(text(f"SELECT getAgeRestrictorFilms(:film_id)"),
                                      {"film_id": film_id})

        return film_age <= curent_age

@app.route('/access_series/<int:series_id>', endpoint="access_series", methods=['GET'])
@jwt_required
def access(series_id):
    """
    These 2 functions grant or deny acces to the film or series,
    depending on the profile age and films restriction
    """
    user_id = get_jwt_identity()
    with sessions[user_id].connect() as connection:
        profile_id = get_jwt_identity()

        curent_age = connection.execute(text(f"SELECT getAgeProfile(:profile_id)"),
                                        {"profile_id": profile_id})

        series_age = connection.execute(text(f"SELECT getAgeRestrictorSeries(:series_id);"),
                                        {"series_id": series_id})

        return series_age <= curent_age

with app.test_request_context():
    spec.path(view=login)
