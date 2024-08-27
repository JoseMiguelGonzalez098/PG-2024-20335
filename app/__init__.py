from flask import Flask
from app.config import Config
from .models import db
from flask_migrate import Migrate
from .routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Registrar los Blueprints
    app.register_blueprint(user_bp)

    return app
