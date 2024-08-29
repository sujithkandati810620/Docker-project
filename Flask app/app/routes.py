from flask import Blueprint, request, jsonify
from .db.postgresql import pg_cursor, pg_conn
from psycopg2 import sql

main_bp = Blueprint('main', __name__)

@main_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json

    required_fields = ['username', 'email', 'password', 'address', 'age', 'phone']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    email = data['email']

    try:
        pg_cursor.execute(
            sql.SQL("SELECT 1 FROM users WHERE email = %s"),
            [email]
        )
        existing_user_pg = pg_cursor.fetchone()
        if existing_user_pg:
            return jsonify({"error": "Email already exists in PostgreSQL"}), 400

        pg_cursor.execute(
            sql.SQL("INSERT INTO addresses (address) VALUES (%s) RETURNING id"),
            [data['address']]
        )
        address_id = pg_cursor.fetchone()[0]

        pg_cursor.execute(
            sql.SQL("INSERT INTO phones (phone) VALUES (%s) RETURNING id"),
            [data['phone']]
        )
        phone_id = pg_cursor.fetchone()[0]

        pg_cursor.execute(
            sql.SQL("INSERT INTO ages (age) VALUES (%s) RETURNING id"),
            [data['age']]
        )
        age_id = pg_cursor.fetchone()[0]

        pg_cursor.execute(
            sql.SQL("""
                INSERT INTO users (username, email, password, address_id, phone_id, age_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """),
            [data['username'], data['email'], data['password'], address_id, phone_id, age_id]
        )
        user_id_pg = pg_cursor.fetchone()[0]
        pg_conn.commit()

        return jsonify({"user_id": str(user_id_pg)}), 201
    except Exception as e:
        pg_conn.rollback()
        return jsonify({"error": str(e)}), 500
