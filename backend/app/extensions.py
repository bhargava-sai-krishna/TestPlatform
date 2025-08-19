from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()

def init_cors(app, origins: list[str]):
    CORS(app, resources={r"/api/*": {"origins": origins}}, supports_credentials=True)
