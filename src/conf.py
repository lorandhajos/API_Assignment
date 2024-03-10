import os
import random
import string

from sqlalchemy import text

from blueprints.utils import get_db_engine, check_env_vars

def init_database():
    engine = get_db_engine(f"{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}")
    username = "api_user"
    password = ''.join(random.choice(string.ascii_letters) for i in range(15))
    with engine.connect() as connection:
        # sql alchemy does not support bind parameters for DDL statements
        connection.execute(text(f"ALTER USER {username} WITH PASSWORD '{password}'"))
        connection.commit()
    os.environ['API_USER_PASS'] = password
    os.environ['API_USER_NAME'] = username

def on_starting(server):
    required = ["DB_NAME", "DB_USER", "DB_PASS", "API_VERSION", "JWT_SECRET_KEY", "SECRET_KEY"]

    if check_env_vars(required):
        init_database()
    else:
        raise Exception("Failed to start server! Environmental variables not configured!")
