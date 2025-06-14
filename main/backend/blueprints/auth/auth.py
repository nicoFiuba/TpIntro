from flask import Blueprint, request, jsonify, session
from db import get_connection
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def user_exists(username):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM Usuario WHERE username = %s", (username,))
            return cursor.fetchone() is not None
        
def create_user(username, password, email=None, role="user"):
    hashed_password = generate_password_hash(password)
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Usuario (username, password_,email, role) VALUES (%s, %s, %s, %s)",
                (username, hashed_password, email, role)
            )
            conn.commit()

def verify_user(username, password):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Usuario WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user["password_"], password):
                return user
            return None
        
def get_user_by_username(username):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Usuario WHERE username = %s", (username,))
            return cursor.fetchone()
       