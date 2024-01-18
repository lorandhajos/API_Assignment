import os
from datetime import timedelta

from apispec import APISpec
from dotenv import load_dotenv
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, render_template, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, get_jwt_identity,
                                jwt_required)
from marshmallow import Schema, fields
from sqlalchemy import create_engine, text

if os.environ.get('FLASK_ENV') == 'development':
    load_dotenv("../.env")

spec = APISpec(
    title = "Netflix API",
    version = f"{os.environ['API_VERSION']}.0.0",
    openapi_version = "3.1.0",
    plugins = [FlaskPlugin(), MarshmallowPlugin()],
    info = dict(
        description="Netflix API",
    ),
    servers = [dict(url=f"/api/{os.environ['API_VERSION']}")],
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

class WatchlistSchema(Schema):
    film = fields.List(fields.Integer(), required=True)
    series = fields.List(fields.Integer(), required=True)

api_key_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
spec.components.security_scheme("JWT", api_key_scheme)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

sessions = {}

def get_db_engine(user, password):
    if os.environ.get('FLASK_ENV') == 'development':
        return create_engine(f"postgresql+psycopg://{user}:{password}@localhost:5432/{os.environ['DB_NAME']}", echo=True)
    else:
        return create_engine(f"postgresql+psycopg://{user}:{password}@db:5432/{os.environ['DB_NAME']}", echo=True)

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
    engine = get_db_engine(os.environ['DB_USER'], os.environ['DB_PASS'])
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
    ---
    post:
        description: Token refresh endpoint
        security:
            - JWT: []
        responses:
            200:
                description: Token refresh successful
                content:
                    application/json:
                        schema: LoginResponseSchema
    """
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)

    return jsonify(access_token=new_token)

@app.route('/watchlist/<int:watchlist_id>', methods=['GET'])
@jwt_required(optional=False)
def watchlist(watchlist_id):
    """
    Returns the watchlist
    ---
    get:
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

        return WatchlistSchema().dump(result)

@app.route('/history/<int:history_id>', endpoint="history", methods=['GET'])
@jwt_required(optional=False)
def history(history):
    """
    Returns full history in the same format as the watchlist function
    ---
    get:
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

@app.route('/access_films/<int:film_id>', endpoint="access_films", methods=['GET'])
@jwt_required(optional=False)
def access_films(film_id):
    """
    These 2 functions grant or deny access to the film or series,
    depending on the profile age and films restriction
    ---
    get:
        description: These 2 functions grant or deny access to the film or series, depending on the profile age and films restriction
        security:
            - JWT: []
        parameters:
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
                        schema: WatchlistSchema
            401:
                description: Access denied
                content:
                    application/json:
                        schema: ErrorResponseSchema
    """
    user_id = get_jwt_identity()
    with sessions[user_id].connect() as connection:
        profile_id = get_jwt_identity()

        curent_age = connection.execute(text(f"SELECT getAgeProfile(:profile_id);"),
                                        {"profile_id": profile_id})

        film_age = connection.execute(text(f"SELECT getAgeRestrictorFilms(:film_id)"),
                                      {"film_id": film_id})

        return jsonify(film_age <= curent_age)

@app.route('/access_series/<int:series_id>', endpoint="access_series", methods=['GET'])
@jwt_required(optional=False)
def access_series(series_id):
    """
    These 2 functions grant or deny access to the film or series,
    depending on the profile age and films restriction
    ---
    get:
        description: These 2 functions grant or deny access to the film or series, depending on the profile age and films restriction
        security:
            - JWT: []
        parameters:
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
                        schema: WatchlistSchema
            401:
                description: Access denied
                content:
                    application/json:
                        schema: ErrorResponseSchema
    """
    user_id = get_jwt_identity()
    with sessions[user_id].connect() as connection:
        curent_age = connection.execute(text(f"SELECT getAgeProfile(:profile_id)"),
                                        {"profile_id": user_id})

        series_age = connection.execute(text(f"SELECT getAgeRestrictorSeries(:series_id);"),
                                        {"series_id": series_id})

        return jsonify(series_age <= curent_age)

@app.route('/views_report_films', endpoint='views_report_films', methods=['GET'])
@jwt_required(optional=False)
def views_report_films():
    """
    These 2 functions fetch a total view count with the name
    ---
    get:
        description: These 2 functions fetch a total view count with the name
        security:
            - JWT: []
        responses:
            200:
                description: Total view count returned
                content:
                    application/json:
                        schema: WatchlistSchema
    """
    user_id = get_jwt_identity()
    with sessions[user_id].connect() as connection:

        totalViewCount = connection.execute(text(f"SELECT getMovieViews()"))

    return jsonify(totalViewCount)

@app.route('/views_report_series', endpoint='views_report_series', methods=['GET'])
@jwt_required(optional=False)
def views_report_series():
    """
    These 2 functions fetch a total view count with the name
    ---
    get:
        description: These 2 functions fetch a total view count with the name
        security:
            - JWT: []
        responses:
            200:
                description: Total view count returned
                content:
                    application/json:
                        schema: WatchlistSchema
    """
    user_id = get_jwt_identity()
    with sessions[user_id].connect() as connection:
        totalViewCount = connection.execute(text(f"SELECT getSeriesViews()"))

    return jsonify(totalViewCount)

@app.route('/country_report', endpoint='country_report', methods=['GET'])
@jwt_required(optional=False)
def country_report():
    """
    This is the function which returns the total count of the countries
    ---
    get:
        description: This is the function which returns the total count of the countries
        security:
            - JWT: []
        responses:
            200:
                description: Total count of the countries returned
                content:
                    application/json:
                        schema: WatchlistSchema
    """
    user_id = get_jwt_identity()
    with sessions[user_id].connect() as connection:

        countryCount = connection.execute(text(f"SELECT getProfileCountry()"))

    return jsonify(countryCount)

with app.test_request_context():
    spec.path(view=login)
    spec.path(view=refresh)
    spec.path(view=watchlist)
    spec.path(view=history)
    spec.path(view=access_films)
    spec.path(view=access_series)
    spec.path(view=views_report_films)
    spec.path(view=views_report_series)
    spec.path(view=country_report)
