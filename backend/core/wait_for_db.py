import time
from django.db import connections
from django.db.utils import OperationalError

def wait_for_db():
    db_conn = None

    while not db_conn:
        try:
            db_conn = connections['default']
            db_conn.cursor()
            print("DB is ready")
        except OperationalError:
            print("DB not ready, waiting...")
            time.sleep(2)