from flask import session, jsonify
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'No autenticado'}), 401
        if not session.get('is_admin'):
            return jsonify({'message': 'Acceso solo disponible para administradores'}), 403
        return f(*args, **kwargs)
    return decorated_function

