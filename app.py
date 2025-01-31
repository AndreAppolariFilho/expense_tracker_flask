from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("APPLICATION_SECRET_KEY", "SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URL", 'sqlite:///expenses.db')
app.config["JWT_SECRET_KEY"] = os.environ.get("APPLICATION_JWT_SECRET_KEY", 'your_jwt_secret_key')
app.config['JWT_TOKEN_LOCATION'] = ['headers']
db = SQLAlchemy(app)
# JWT Initialization
jwt = JWTManager(app)
migrate = Migrate(app, db)

