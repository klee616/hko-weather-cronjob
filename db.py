# db.py
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from config import DB_CONFIG

# Initialize the connection pool (minimum 1 connection, maximum 10 connections).
db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, **DB_CONFIG)

@contextmanager
def get_db_connection():
    """Use a Context Manager to borrow and return a connection."""
    conn = db_pool.getconn()
    try:
        yield conn
    finally:
        db_pool.putconn(conn)

def close_all_connections():
    """Release the connection pool when the project shuts down."""
    db_pool.closeall()