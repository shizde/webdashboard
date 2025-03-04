# This file ensures that the src directory is treated as a Python package
# It can be used to configure any package-level imports or configurations

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Create application-wide instances
app = Flask(__name__)
CORS(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Import models to ensure they are registered with SQLAlchemy
from .models.user import User
from .models.expense import Expense
from .models.event import Event

# You can add any global configurations or initializations here
def init_app():
    # Configure app settings
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/expense_tracker'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    
    return app