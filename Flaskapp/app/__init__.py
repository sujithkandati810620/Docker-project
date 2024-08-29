from flask import Flask
from flask_cors import CORS
from .db.postgresql import pg_conn, pg_cursor
from .routes import main_bp


def create_app():
    app = Flask(__name__)
    
    # Call the function to create tables
    create_tables()
    CORS(app)

    app.register_blueprint(main_bp)
    
    return app

def create_tables():
    try:
        # Create addresses table
        pg_cursor.execute("""
            CREATE TABLE IF NOT EXISTS addresses (
                id SERIAL PRIMARY KEY,
                address VARCHAR(255) NOT NULL
            )
        """)

        # Create phones table
        pg_cursor.execute("""
            CREATE TABLE IF NOT EXISTS phones (
                id SERIAL PRIMARY KEY,
                phone VARCHAR(20) NOT NULL
            )
        """)

        # Create ages table
        pg_cursor.execute("""
            CREATE TABLE IF NOT EXISTS ages (
                id SERIAL PRIMARY KEY,
                age INTEGER NOT NULL
            )
        """)

        # Create users table
        pg_cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                address_id INTEGER REFERENCES addresses(id),
                phone_id INTEGER REFERENCES phones(id),
                age_id INTEGER REFERENCES ages(id)
            )
        """)

        # Commit the changes to the database
        pg_conn.commit()

    except Exception as e:
        # Rollback in case of any error
        pg_conn.rollback()
        print(f"Error creating tables: {e}")

