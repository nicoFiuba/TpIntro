from flask import Blueprint, session, jsonify, request

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'No autenticado'}), 401
        if not session.get("is_admin"):
            return jsonify({'message': 'Acceso solo disponible para aminisstradores'})
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    return jsonify({
        "message": f"Panel de administración para el usuario con ID {session['user_id']}",
    }), 200