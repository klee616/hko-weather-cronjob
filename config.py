# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", os.getenv("host")),
    "dbname": os.getenv("DB_NAME", os.getenv("dbname", os.getenv("database"))),
    "user": os.getenv("DB_USER", os.getenv("user")),
    "password": os.getenv("DB_PASSWORD", os.getenv("password")),
    "port": os.getenv("DB_PORT", os.getenv("port", "5432")),
}