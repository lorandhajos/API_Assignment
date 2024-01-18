import os

from dotenv import load_dotenv
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from api import app as api_app
from frontend import app as frontend_app

application = DispatcherMiddleware(frontend_app, {
    f'/api/{os.environ["API_VERSION"]}': api_app
})

if __name__ == '__main__':
    load_dotenv("../.env")
    os.environ['FLASK_ENV'] = 'development'
    run_simple('localhost', 5000, application, use_reloader=True, use_debugger=True)
