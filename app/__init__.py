from flask import Flask
from app.config import Config
from .models import db
from flask_migrate import Migrate

from .routes.user_routes import user_bp
from .routes.traduction_routes import traduction_bp
from .routes.video_routes import video_bp
from app.routes.dictionary_routes import dictionary_bp
from app.routes.profile_routes import profile_bp
from .mailer import mail

from .mailer import init_mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Inicializar Flask-Mail
    init_mail(app)

    # Registrar los Blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(traduction_bp)
    app.register_blueprint(video_bp)
    app.register_blueprint(dictionary_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(mail)

    return app
