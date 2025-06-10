from flask import Blueprint, request, jsonify, session, redirect
from functools import wraps

from blueprints.auth.auth import user_exists, create_user, verify_user
from blueprints.admin.admin import admin_required
from blueprints.user.user import login_required, get_user_by_id

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')


    if not username or not password:
        return jsonify({'message': 'Faltan datos'}), 400
    if user_exists(username):
        return jsonify({'message': 'Usuario ya existe'}), 400
    
    create_user(username, password, email)
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

    if not request.is_json:
        return redirect('http://localhost:8080/my-account')

    return jsonify({'message': 'Inicio de sesión exitoso', 'user_id': user['id']}), 200

@usuarios_bp.route('/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Sesión cerrada exitosamente'}), 200

@usuarios_bp.route('/user/profile', methods=['GET'])
@login_required
def profile():
    user_id = session["user_id"]
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    
@usuarios_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id_endpoint(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

@usuarios_bp.route('/admin/dashboard', methods=['GET'])
@admin_required
def dashboard():
    return jsonify({'message': f'Panel de administración para el usuario con ID {session["user_id"]}'}), 200

@usuarios_bp.route('/admin/create_admin', methods=['POST'])
@admin_required
def create_admin_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password:
        return jsonify({'message': 'Faltan datos'}), 400
    if user_exists(username):
        return jsonify({'message': 'Usuario ya existe'}), 400
    create_user(username, password, email=None, role='admin')
    return jsonify({'message': f'Administrador creado exitosamente'}), 201

@usuarios_bp.route('/auth/status', methods=['GET'])
def session_status():
    if 'user_id' in session:
        return jsonify({'authenticated': True, 'user_id': session['user_id'], 'is_admin': session.get('is_admin', False)})
    return jsonify({'authenticated': False}), 200



