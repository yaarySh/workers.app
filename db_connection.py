# db_connection.py
import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    conn = psycopg2.connect(
        dbname="workers_db",
        user="workers_db_user",
        password="pnIiMaDy33oElZab5YklZUSiWX0sTy8q",
        host="dpg-cr88poaj1k6c739qmscg-a.oregon-postgres.render.com",
        port="5432",
        cursor_factory=RealDictCursor,  # Add this line
    )
    return conn
