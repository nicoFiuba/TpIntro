from flask import Flask, Blueprint
from flask_cors import CORS
import config

from blueprints.usuarios.auth import auth_bp
from blueprints.usuarios.user import user_bp
from blueprints.usuarios.admin import admin_bp
from blueprints.catalogo import productos_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/product')
    app.register_blueprint(productos_bp, url_prefix='/catalogo')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)