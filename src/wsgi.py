import os

from flask_cors import CORS
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from api import app as api_app
from frontend import app as frontend_app

os.environ['FLASK_ENV'] = 'production'

CORS(frontend_app)
CORS(api_app)

application = DispatcherMiddleware(frontend_app, {
    f'/api/{os.environ["API_VERSION"]}': api_app
})

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    run_simple('localhost', 5000, application, use_reloader=True, use_debugger=True)
