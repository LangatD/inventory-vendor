from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from dotenv import load_dotenv
from app.extensions import db
from app.models import create_tables
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

import os

load_dotenv()



def create_app():
    app = Flask(__name__)
    CORS(app)

    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("POSTGRES_DB")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    app.config['JWT_SECRET_KEY'] = 'inventory2030'  
    app.config['JWT_TOKEN_LOCATION'] = ['headers']  
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'

    

    
    
    db.init_app(app)
  
    JWTManager(app)

    
    from app.routes import vendor_bp
    app.register_blueprint(vendor_bp, url_prefix="/vendors")
    #print(app.url_map)
    with app.app_context():
        create_tables()
    
    return app
