from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(app)

from app import models
with app.app_context():
    db.create_all()

from app import routes