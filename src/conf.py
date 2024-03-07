import os
import random
import string

from sqlalchemy import text

from blueprints.utils import get_db_engine

def init_database():
    try:
        engine = get_db_engine(f"{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}")
        username = "api_user"
        password = ''.join(random.choice(string.ascii_letters) for i in range(15))
        with engine.connect() as connection:
            # sql alchemy does not support bind parameters for DDL statements
            connection.execute(text(f"ALTER USER {username} WITH PASSWORD '{password}'"))
            connection.commit()
        os.environ['API_USER_PASS'] = password
        os.environ['API_USER_NAME'] = username
    except Exception:
        raise Exception("Filed to initialize database")

def on_starting(server):
    init_database()
