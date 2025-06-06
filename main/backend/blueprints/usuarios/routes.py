from flask import Blueprint, request, jsonify, session
from functools import wraps

from blueprints.usuarios.auth import user_exists, create_user, verify_user
from blueprints.usuarios.admin import admin_required
from blueprints.usuarios.user import login_required

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Faltan datos'}), 400
    if user_exists(username):
        return jsonify({'message': 'Usuario ya existe'}), 400
    
    create_user(username, password)
    return jsonify({'message': 'Usuario creado exitosamente'}), 201

@usuarios_bp.route('/auth/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

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

@usuarios_bp.route('/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Sesión cerrada exitosamente'}), 200

@usuarios_bp.route('/user/profile', methods=['GET'])
@login_required
def profile():
    return jsonify({'message': f'Perfil de usuario con ID {session["user_id"]}'}), 200

@usuarios_bp.route('/admin/dashboard', methods=['GET'])
@admin_required
def dashboard():
    return jsonify({'message': f'Panel de administración para el usuario con ID {session["user_id"]}'}), 200

@usuarios_bp.route('admin/create_admin', methods=['POST'])
@admin_required
def create_admin_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Faltan datos'}), 400
    if user_exists(username):
        return jsonify({'message': 'Usuario ya existe'}), 400
    create_user(username, password, role='admin')
    return jsonify({'message': f'Administrador creado exitosamente'}), 201

