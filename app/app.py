from flask import Flask, jsonify, request
from .auth import auth_bp, jwt
from .user import user_bp
from .import schemas, models
from app.database import engine, get_db
from datetime import timedelta
import os
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)

    load_dotenv()

    # Defining encryption keys for jwt token
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=45)

    # Initialize JWT Manager with app
    jwt.init_app(app)

    # Initiallize daatabase with designed models
    models.Base.metadata.create_all(bind=engine)

    # Registering Blueprints for the app
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')


    @app.route('/', methods=["GET"])
    def root():
        return "<h1>flask JWT</h1>"
    
    return app;

