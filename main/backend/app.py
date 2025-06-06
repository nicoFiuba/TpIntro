from flask import Flask, Blueprint
from flask_cors import CORS
import config

from blueprints.usuarios.routes import usuarios_bp
from blueprints.catalogo import productos_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = config.SECRET_KEY

    CORS(app)

    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(productos_bp, url_prefix='/catalogo')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)