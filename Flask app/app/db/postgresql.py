import psycopg2
from ..config import Config

pg_conn = psycopg2.connect(
    dbname=Config.POSTGRES_DB,
    user=Config.POSTGRES_USER,
    password=Config.POSTGRES_PASSWORD,
    host=Config.POSTGRES_HOST,
    port=Config.POSTGRES_PORT
)
pg_cursor = pg_conn.cursor()
