from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.models import Visitor
    with app.app_context():
        db.create_all()

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
