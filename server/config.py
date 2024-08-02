from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import secrets


db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job-board.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)

migrate = Migrate(app, db)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

db.init_app(app)

bcrypt = Bcrypt()

app.register_blueprint(api_bp, url_prefix='/api')

CORS(app)





