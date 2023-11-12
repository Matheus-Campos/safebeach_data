import os
import psycopg2 as pg

def connect():
    db_host = os.getenv('DB_HOST', 'db')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'root')
    db_name = os.getenv('DB_NAME', 'safebeach')
    return pg.connect(host=db_host, user=db_user, password=db_password, database=db_name)
