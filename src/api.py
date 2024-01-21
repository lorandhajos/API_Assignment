import os
from datetime import timedelta

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_jwt_extended import JWTManager
from marshmallow import Schema, fields

from blueprints.account import Account, Profile, Subscription
from blueprints.genre import Genre
from blueprints.login import Login
from blueprints.movies import Movies
from blueprints.profile import (AccessFilms, AccessSeries, History, Interests,
                                Preferences, Watchlist)
from blueprints.report import (Country, FilmNames, FilmViews, SeriesNames,
                               SeriesViews)
from blueprints.series import Series
from blueprints.token import Token

class ErrorResponseSchema(Schema):
    msg = fields.String(required=True)

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

api_key_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
spec.components.security_scheme("JWT", api_key_scheme)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

# Account
account_view_get = Account.as_view('account_get')
account_view_post = Account.as_view('account_post')
account_view_crud = Account.as_view('account_crud')

app.add_url_rule('/account/', defaults={'id': None}, view_func=account_view_get, methods=['GET',])
app.add_url_rule('/account/', view_func=account_view_post, methods=['POST',])
app.add_url_rule('/account/<int:id>', view_func=account_view_crud, methods=['GET', 'PUT', 'DELETE'])

account_profile_view_get = Profile.as_view('account_profile_get')
account_profile_view_post = Profile.as_view('account_profile_post')
account_profile_view_crud = Profile.as_view('account_profile_crud')

app.add_url_rule('/profile/', defaults={'id': None}, view_func=account_profile_view_get, methods=['GET',])
app.add_url_rule('/profile/', view_func=account_profile_view_post, methods=['POST',])
app.add_url_rule('/profile/<int:id>', view_func=account_profile_view_crud, methods=['GET', 'PUT', 'DELETE'])

account_subscription_view_get = Subscription.as_view('account_subscription_get')
account_subscription_view_post = Subscription.as_view('account_subscription_post')
account_subscription_view_crud = Subscription.as_view('account_subscription_crud')

app.add_url_rule('/subscription/', defaults={'id': None}, view_func=account_subscription_view_get, methods=['GET',])
app.add_url_rule('/subscription/', view_func=account_subscription_view_post, methods=['POST',])
app.add_url_rule('/subscription/<int:id>', view_func=account_subscription_view_crud, methods=['GET', 'PUT', 'DELETE'])

# Genre
genre_view_get = Genre.as_view('genre_get')
genre_view_post = Genre.as_view('genre_post')
genre_view_crud = Genre.as_view('genre_crud')

app.add_url_rule('/genre/', defaults={'id': None}, view_func=genre_view_get, methods=['GET',])
app.add_url_rule('/genre/', view_func=genre_view_post, methods=['POST',])
app.add_url_rule('/genre/<int:id>', view_func=genre_view_crud, methods=['GET', 'PUT', 'DELETE'])

# Movies
movies_view_get = Movies.as_view('movies_get')
movies_view_post = Movies.as_view('movies_post')
movies_view_crud = Movies.as_view('movies_crud')

app.add_url_rule('/movies/', defaults={'id': None}, view_func=movies_view_get, methods=['GET',])
app.add_url_rule('/movies/', view_func=movies_view_post, methods=['POST',])
app.add_url_rule('/movies/<int:id>', view_func=movies_view_crud, methods=['GET', 'PUT', 'DELETE'])

# Series
series_view_get = Series.as_view('series_get')
series_view_post = Series.as_view('series_post')
series_view_crud = Series.as_view('series_crud')

app.add_url_rule('/series/', defaults={'id': None}, view_func=series_view_get, methods=['GET',])
app.add_url_rule('/series/', view_func=series_view_post, methods=['POST',])
app.add_url_rule('/series/<int:id>', view_func=series_view_crud, methods=['GET', 'PUT', 'DELETE'])

# Profile
history_view_get = History.as_view('history_get')
history_view_post = History.as_view('history_post')
history_view_crud = History.as_view('history_crud')

app.add_url_rule('/history/', defaults={'id': None}, view_func=history_view_get, methods=['GET',])
app.add_url_rule('/history/', view_func=history_view_post, methods=['POST',])
app.add_url_rule('/history/<int:id>', view_func=history_view_crud, methods=['GET', 'PUT', 'DELETE'])

interests_view_get = Interests.as_view('interests_get')
interests_view_post = Interests.as_view('interests_post')
interests_view_crud = Interests.as_view('interests_crud')

app.add_url_rule('/interests/', defaults={'id': None}, view_func=interests_view_get, methods=['GET',])
app.add_url_rule('/interests/', view_func=interests_view_post, methods=['POST',])
app.add_url_rule('/interests/<int:id>', view_func=interests_view_crud, methods=['GET', 'PUT', 'DELETE'])

preferences_view_get = Preferences.as_view('preferences_get')
preferences_view_post = Preferences.as_view('preferences_post')
preferences_view_crud = Preferences.as_view('preferences_crud')

app.add_url_rule('/preferences/', defaults={'id': None}, view_func=preferences_view_get, methods=['GET',])
app.add_url_rule('/preferences/', view_func=preferences_view_post, methods=['POST',])
app.add_url_rule('/preferences/<int:id>', view_func=preferences_view_crud, methods=['GET', 'PUT', 'DELETE'])

access_films_view = AccessFilms.as_view('access_films')
app.add_url_rule('/profile/<int:profile_id>/access_films/<int:film_id>', view_func=access_films_view, methods=['GET',])

access_series_view = AccessSeries.as_view('access_series')
app.add_url_rule('/profile/<int:profile_id>/access_series/<int:series_id>', view_func=access_series_view, methods=['GET',])

watchlist_view_get = Watchlist.as_view('watchlist_get')
watchlist_view_post = Watchlist.as_view('watchlist_post')
watchlist_view_crud = Watchlist.as_view('watchlist_crud')

app.add_url_rule('/watchlist/', defaults={'id': None}, view_func=watchlist_view_get, methods=['GET',])
app.add_url_rule('/watchlist/', view_func=watchlist_view_post, methods=['POST',])
app.add_url_rule('/watchlist/<int:id>', view_func=watchlist_view_crud, methods=['GET', 'PUT', 'DELETE'])

# Report
views_report_films_names = FilmNames.as_view('views_report_films_names')
app.add_url_rule("/report/views_report_films_names", view_func=views_report_films_names, methods=['GET'])

views_report_films_views = FilmViews.as_view('views_report_films_views')
app.add_url_rule("/report/views_report_films_views", view_func=views_report_films_views, methods=['GET'])

views_report_series_title = SeriesNames.as_view('views_report_series_title')
app.add_url_rule("/report/views_report_series_title", view_func=views_report_series_title, methods=['GET'])

views_report_series_views = SeriesViews.as_view('views_report_series_views')
app.add_url_rule("/report/views_report_series_views", view_func=views_report_series_views, methods=['GET'])

country_view = Country.as_view('country')
app.add_url_rule("/report/country", view_func=country_view, methods=['GET'])

# Login
login_view = Login.as_view('login')
app.add_url_rule("/login", view_func=login_view, methods=['POST'])

# Token
refresh_view = Token.as_view('refresh')
app.add_url_rule("/token_refresh", view_func=refresh_view, methods=['POST'])

# Swagger
with app.test_request_context():
    # Account
    spec.path(view=account_view_get)
    spec.path(view=account_view_post)
    spec.path(view=account_view_crud)

    spec.path(view=account_profile_view_get)
    spec.path(view=account_profile_view_post)
    spec.path(view=account_profile_view_crud)

    spec.path(view=account_subscription_view_get)
    spec.path(view=account_subscription_view_post)
    spec.path(view=account_subscription_view_crud)

    # Genre
    spec.path(view=genre_view_get)
    spec.path(view=genre_view_post)
    spec.path(view=genre_view_crud)

    # Movies
    spec.path(view=movies_view_get)
    spec.path(view=movies_view_post)
    spec.path(view=movies_view_crud)

    # Series
    spec.path(view=series_view_get)
    spec.path(view=series_view_post)
    spec.path(view=series_view_crud)

    # Profile
    spec.path(view=history_view_get)
    spec.path(view=history_view_post)
    spec.path(view=history_view_crud)

    spec.path(view=interests_view_get)
    spec.path(view=interests_view_post)
    spec.path(view=interests_view_crud)

    spec.path(view=preferences_view_get)
    spec.path(view=preferences_view_post)
    spec.path(view=preferences_view_crud)

    spec.path(view=access_films_view)

    spec.path(view=access_series_view)

    spec.path(view=watchlist_view_get)
    spec.path(view=watchlist_view_post)
    spec.path(view=watchlist_view_crud)

    # Report
    spec.path(view=views_report_films_names)
    spec.path(view=views_report_films_views)
    spec.path(view=views_report_series_title)
    spec.path(view=views_report_series_views)
    spec.path(view=country_view)

    # Login
    spec.path(view=login_view)

    # Token
    spec.path(view=refresh_view)

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
