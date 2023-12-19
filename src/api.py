from ast import JoinedStr
from crypt import methods
from datetime import timedelta
from operator import truediv
import re

from dotenv import dotenv_values
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token, jwt_refresh_token_required, get_jwt_identity
from sqlalchemy import create_engine, text

config = dotenv_values("../.env")

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config['JWT_SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)
engine = create_engine(f"postgresql+psycopg://{config['DB_USER']}:{config['DB_PASS']}@localhost:5432/{config['DB_NAME']}", echo=True)

# Generate a refresh token
def generate_refresh_token(user_id):
    refresh_token = create_refresh_token(identity=user_id)
    return refresh_token

def generate_token(user_id):
    token = create_access_token(identity=user_id)
    return token

@app.route('/login', methods=['POST'])
def login():
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT account_id FROM account WHERE email = :email AND password = :password"),
                                    {"email": request.json.get('email'), "password": request.json.get('password')})
        if result.rowcount == 0:
            return jsonify({"msg": "Bad username or password"}), 401

        user_id = result.first()._asdict().get('id')
        token = generate_token(user_id)
        return jsonify(access_token=token)

@app.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    new_token = generate_token(current_user)
    return jsonify(access_token=new_token)

@app.route('/account', methods=['GET'])
@jwt_required()
def account():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM account"))
        result_list = []
        for row in result:
            result_list.append(row._asdict())

        return jsonify(result_list)


@app.route('/watchlist/<int:wathclist_id>/', methods=['GET'])
@jwt_required
def watchlist(wathclist_id):
    result = [[], []]

    resultFilms = connection.execute(text(f"SELECT movie_id FROM wathclist_movies WHERE wathclist_id = :wathclist_id"))

    if resultFilms.rowcount!=0:
        for film in resultFilms:
            result[0].append(film._asdict())

    resultSeries = connection.execute(text(f"SELECT series_id FROM wathclist_series WHERE wathclist_id = :wathclist_id"))

    if resultSeries.rowcount!=0:
        for series in resultSeries:
            result[1].append(series._asdict())

    return jsonify(result)
    # Returns the full watchlist in a nice json format, first element of this 2d array is always films, second is always series

@app.route('history/<int:history_id>', methods=['GET'])
@jwt_required
def history(history):
    result = [[], []]

    resultFilms = connection.execute(text(f"SELECT movie_id FROM history_movies WHERE history_id = " + history))

    if resultFilms.rowcount!=0:
        for film in resultFilms:
            result[0].append(film._asdict())

    resultSeries = connection.execute(text(f"SELECT series_id FROM history_series WHERE history_id = " + history))

    if resultSeries.rowcount!=0:
        for series in resultSeries:
            result[1].append(series._asdict())
    
    return jsonify(result)
    # Returns full history in the same format as the watchlist function
    
@app.route('access_films/<int:film_id>', methods=['GET'])
@jwt_required
def acces(film_id):
    profile_id = get_jwt_identity()

    curent_age = connection.execute(text(f"SELECT age FROM profile WHERE profile_id =" + profile_id))

    film_age = connection.execute(text(f"SELECT age_restrictor FROM genre INNER JOIN movie_genre ON film_id WHERE film_id = " + film_id))

    return film_age<= curent_age
        
@app.route('access_series/<int:series_id>', methods=['GET'])
@jwt_required
def acces(series_id):
    profile_id = get_jwt_identity()

    curent_age = connection.execute(text(f"SELECT age FROM profile WHERE profile_id =" + profile_id))

    series_age = connection.execute(text(f"SELECT age_restrictor FROM genre INNER JOIN series_genre ON series_id WHERE series_id = " + series_id))

    return series_age<=curent_age
    
# These 2 functions grant or deny acces to the film or series, depending on the profile age and films restriction