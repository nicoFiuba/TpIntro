from flask import Blueprint, request, jsonify, session
from db import get_connection
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint('auth', __name__)

def user_exists(username):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE username = %s. (username,)")
            return cursor.fetchone() is not None
        
def create_user(username, password, role="user"):
    hashed_password = generate_password_hash(password)
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, hashed_password, role)
            )
            conn.commit()

def verify_user(username, password):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user["password"], password):
                return user
            return None
        
    @auth_bp.route('/register', methods=['POST'])
    def register():
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Faltan datos'}), 400
        if user_exists(username):
            return jsonify({'message': 'Usuario ya existe'}), 400
        create_user(username, password)
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Faltan datos'}), 400
        user = verify_user(username, password)
        if not user:
            return jsonify({'message': 'Credenciales incorrectas'}), 401
        
        session['user_id'] = user['id']
        session['is_admin'] = user['role'] == 'admin'
        
        return jsonify({'message': 'Inicio de sesión exitoso', 'user_id': user['id']}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Sesión cerrada exitosamente'}), 200    