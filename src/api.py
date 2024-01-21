import json
import os
from base64 import b64encode, b64decode
from datetime import timedelta

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from Crypto.Cipher import ChaCha20
from dotenv import load_dotenv
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
    username = fields.String(required=True)
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

key = b64decode(os.environ['SECRET_KEY'])

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

jwt = JWTManager(app)

def get_db_engine(data):
    if os.environ.get('FLASK_ENV') == 'development':
        return create_engine(f"postgresql+psycopg://{data}@localhost:5432/{os.environ['DB_NAME']}", echo=True)
    else:
        return create_engine(f"postgresql+psycopg://{data}@db:5432/{os.environ['DB_NAME']}", echo=True)

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
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        data = f"{username}:{password}"

        engine = get_db_engine(data)
        engine.connect()

        cipher = ChaCha20.new(key=key)
        ciphertext = cipher.encrypt(data.encode('utf-8'))

        nonce = b64encode(cipher.nonce).decode('utf-8')
        ciphertext = b64encode(ciphertext).decode('utf-8')

        result = json.dumps({'nonce': nonce, 'ciphertext': ciphertext})
    except Exception as e:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=result)
    refresh_token = create_refresh_token(identity=result)

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
    data = json.loads(get_jwt_identity())

    nonce = b64decode(data["nonce"])
    ciphertext = b64decode(data["ciphertext"])

    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    engine = get_db_engine(plaintext)
    with engine.connect() as connection:
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

@app.route('/history/<int:history_id>', endpoint="history", methods=['GET'])
@jwt_required(optional=False)
def history(history_id):
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
    data = json.loads(get_jwt_identity())

    nonce = b64decode(data["nonce"])
    ciphertext = b64decode(data["ciphertext"])

    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    engine = get_db_engine(plaintext)
    with engine.connect() as connection:
        result = [[], []]

        resultFilms = connection.execute(text(f"SELECT getHistoryMoviesForID(:history_id);"),
                                         {"history_id": history_id})

        if resultFilms.rowcount != 0:
            for film in resultFilms:
                result[0].append(film._asdict())

        resultSeries = connection.execute(text(f"SELECT getHistorySeriesForID(:history_id);"),
                                            {"history_id": history_id})

        if resultSeries.rowcount != 0:
            for series in resultSeries:
                result[1].append(series._asdict())

        return jsonify(result)

@app.route('/access_films/<int:profile_id>/<int:film_id>', endpoint="access_films", methods=['GET'])
@jwt_required(optional=False)
def access_films(profile_id, film_id):
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
                        schema: WatchlistSchema
            401:
                description: Access denied
                content:
                    application/json:
                        schema: ErrorResponseSchema
    """
    data = json.loads(get_jwt_identity())

    nonce = b64decode(data["nonce"])
    ciphertext = b64decode(data["ciphertext"])

    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    engine = get_db_engine(plaintext)
    with engine.connect() as connection:
        curent_age = connection.execute(text(f"SELECT getAgeProfile(:profile_id);"),
                                        {"profile_id": profile_id}).first()[0]

        film_age = connection.execute(text(f"SELECT getAgeRestrictorFilms(:film_id)"),
                                      {"film_id": film_id}).first()[0]

        return jsonify(film_age <= curent_age)

@app.route('/access_series/<int:profile_id>/<int:series_id>', endpoint="access_series", methods=['GET'])
@jwt_required(optional=False)
def access_series(profile_id, series_id):
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
                        schema: WatchlistSchema
            401:
                description: Access denied
                content:
                    application/json:
                        schema: ErrorResponseSchema
    """
    data = json.loads(get_jwt_identity())

    nonce = b64decode(data["nonce"])
    ciphertext = b64decode(data["ciphertext"])

    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    engine = get_db_engine(plaintext)
    with engine.connect() as connection:
        curent_age = connection.execute(text(f"SELECT getAgeProfile(:profile_id)"),
                                        {"profile_id": profile_id}).first()[0]

        series_age = connection.execute(text(f"SELECT getAgeRestrictorSeries(:series_id);"),
                                        {"series_id": series_id}).first()[0]

        return jsonify(series_age <= curent_age)

@app.route('/views_report_films_names', endpoint='views_report_films_names', methods=['GET'])
@jwt_required(optional=False)
def views_report_films_names():
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
    data = json.loads(get_jwt_identity())

    nonce = b64decode(data["nonce"])
    ciphertext = b64decode(data["ciphertext"])

    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    engine = get_db_engine(plaintext)
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT getMovieNames();")).all()

    totalNames = []

    for name in result:
        totalNames.append({"title" : name[0]})

    return jsonify(totalNames)

@app.route('/views_report_films_views', endpoint='views_report_films_views', methods=['GET'])
@jwt_required(optional=False)
def views_report_films_views():
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
    data = json.loads(get_jwt_identity())

    nonce = b64decode(data["nonce"])
    ciphertext = b64decode(data["ciphertext"])

    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    engine = get_db_engine(plaintext)
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT getMovieViews();")).all()

    totalViews = []

    for view in result:
        totalViews.append({"views" : view[0]})

    return jsonify(totalViews)

@app.route('/views_report_series_title', endpoint='views_report_series_title', methods=['GET'])
@jwt_required(optional=False)
def views_report_series_title():
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
    data = json.loads(get_jwt_identity())

    nonce = b64decode(data["nonce"])
    ciphertext = b64decode(data["ciphertext"])

    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    engine = get_db_engine(plaintext)
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT getSeriesTitle()")).all()

    totalNames = []

    for title in result:
        totalNames.append({"title" : title[0]})

    return jsonify(totalNames)

@app.route('/views_report_series_views', endpoint='views_report_series_views', methods=['GET'])
@jwt_required(optional=False)
def views_report_series_views():
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
    data = json.loads(get_jwt_identity())

    nonce = b64decode(data["nonce"])
    ciphertext = b64decode(data["ciphertext"])

    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    engine = get_db_engine(plaintext)
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT getSeriesViews()")).all()

    totalViews = []

    for title in result:
        totalViews.append({"views" : title[0]})

    return jsonify(totalViews)

@app.route('/country_report_n_of_users', endpoint='country_report_n_of_users', methods=['GET'])
@jwt_required(optional=False)
def country_report_n_of_users():
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
    data = json.loads(get_jwt_identity())

    nonce = b64decode(data["nonce"])
    ciphertext = b64decode(data["ciphertext"])

    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    engine = get_db_engine(plaintext)
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT getNOfUsersPerCountry()")).all()

    totalNumberOfUsers = []

    for number in result:
        totalNumberOfUsers.append({"number" : number[0]})

    return jsonify(totalNumberOfUsers)

@app.route('/country_report_country_of_users', endpoint='country_report_country_of_users', methods=['GET'])
@jwt_required(optional=False)
def country_report_country_of_users():
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
    data = json.loads(get_jwt_identity())

    nonce = b64decode(data["nonce"])
    ciphertext = b64decode(data["ciphertext"])

    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    engine = get_db_engine(plaintext)
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT getUsersCountry()")).all()

    countryOfUsers = []

    for country in result:
        countryOfUsers.append({"country" : country[0]})

    return jsonify(countryOfUsers)

@app.route('/preference_input/<int:inter>/<int:profile_id>', endpoint='preference_input', methods=['POST'])
@jwt_required(optional=False)
def preference_input(inter, profile_id):
    """
    Preference input
    ---
    post:
        description: gggg
        security:
            - JWT: []
        parameters:
            - in: path
              name: inter
              schema:
                type: integer
              required: true
              description: integer id
            - in: path
              name: profile_id
              schema:
                type: integer
              required: true
              description: profile id
        responses:
            200:
                description: Interest inputed
                content:
                    application/json:
                        schema: WatchlistSchema
            400:
                description: Bad data provided
                content:
                    application/json:
                        schema: ErrorResponseSchema
    """
    data = json.loads(get_jwt_identity())

    nonce = b64decode(data["nonce"])
    ciphertext = b64decode(data["ciphertext"])

    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    engine = get_db_engine(plaintext)
    with engine.connect() as connection:
        # result = 
        connection.execute(text(f"CALL inputInterest(:profile_id, :inter);"),
                                            ({"profile_id": profile_id, "inter": inter}))
    return('', 204)

# (text(f"SELECT getAgeRestrictorSeries(:series_id);"),
                                        # {"series_id": series_id}).first()[0]

with app.test_request_context():
    spec.path(view=login)
    spec.path(view=refresh)
    spec.path(view=watchlist)
    spec.path(view=history)
    spec.path(view=access_films)
    spec.path(view=access_series)
    spec.path(view=views_report_films_names)
    spec.path(view=views_report_films_views)
    spec.path(view=views_report_series_views)
    spec.path(view=views_report_series_title)
    spec.path(view=country_report_n_of_users)
    spec.path(view=country_report_country_of_users)
    spec.path(view=preference_input)
