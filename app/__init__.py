from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Configuración para la carga de archivos
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')  # Carpeta donde se guardarán las imágenes
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar las rutas
    from .routes import main
    app.register_blueprint(main)

    return app