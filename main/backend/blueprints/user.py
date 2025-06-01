from flask import Blueprint, session, jsonify

user_bp = Blueprint('user', __name__)
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'No autenticado'}), 401
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/profile')
@login_required
def profile():
    return jsonify({
        "message": f"Perfil de usuario con ID {session['user_id']}",
    }), 200