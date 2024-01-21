import os
from datetime import timedelta

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_jwt_extended import JWTManager
from marshmallow import Schema, fields

from blueprints.account import Login
from blueprints.token import Refresh
from blueprints.profile import Watchlist, History
from blueprints.view import AccessFilms, AccessSeries
from blueprints.report import FilmNames, FilmViews, SeriesNames, SeriesViews, Country

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

# Login
login_view = Login.as_view('login')

app.add_url_rule("/login", view_func=login_view, methods=['POST'])

# Token
refresh_view = Refresh.as_view('refresh')

app.add_url_rule("/token_refresh", view_func=refresh_view, methods=['POST'])

# Profile
watchlist_view = Watchlist.as_view('watchlist')
history_view = History.as_view('history')

app.add_url_rule("/watchlist/<int:watchlist_id>", view_func=watchlist_view, methods=['GET'])
app.add_url_rule("/history/<int:history_id>", view_func=history_view, methods=['GET'])

# View
access_films_view = AccessFilms.as_view('access_films')
access_series_view = AccessSeries.as_view('access_series')

app.add_url_rule("/access_films/<int:profile_id>/<int:film_id>", view_func=access_films_view, methods=['GET'])
app.add_url_rule("/access_series/<int:profile_id>/<int:series_id>", view_func=access_series_view, methods=['GET'])

# Report
views_report_films_names = FilmNames.as_view('views_report_films_names')
views_report_films_views = FilmViews.as_view('views_report_films_views')
views_report_series_title = SeriesNames.as_view('views_report_series_title')
views_report_series_views = SeriesViews.as_view('views_report_series_views')
country_view = Country.as_view('country')

app.add_url_rule("/views_report_films_names", view_func=views_report_films_names, methods=['GET'])
app.add_url_rule("/views_report_films_views", view_func=views_report_films_views, methods=['GET'])
app.add_url_rule("/views_report_series_title", view_func=views_report_series_title, methods=['GET'])
app.add_url_rule("/views_report_series_views", view_func=views_report_series_views, methods=['GET'])
app.add_url_rule("/country", view_func=country_view, methods=['GET'])

with app.test_request_context():
    spec.path(view=login_view)
    spec.path(view=refresh_view)
    spec.path(view=watchlist_view)
    spec.path(view=history_view)
    spec.path(view=access_films_view)
    spec.path(view=access_series_view)
    spec.path(view=views_report_films_names)
    spec.path(view=views_report_films_views)
    spec.path(view=views_report_series_title)
    spec.path(view=views_report_series_views)
    spec.path(view=country_view)

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
