from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

# Create Flask-RESTX API
api = Api(
    title="Flask Demo API",
    version="1.0",
    description="A demo API using Flask and Flask-RESTX",
    doc="/docs",  # Swagger UI available at /docs
)

def create_app():
    app = Flask(__name__)

    # Enable debug mode
    app.config['DEBUG'] = True

    # Configuration
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    # Register Blueprints for non-API routes
    # from .routes.main_routes import main_blueprint  # Import inside create_app to avoid circular import
    # app.register_blueprint(main_blueprint)

    # Initialize the API
    api.init_app(app)

    # Register Namespaces for API routes
    from .routes.auth_routes import auth_ns
    from .routes.item_routes import item_ns
    from .routes.user_routes import user_ns

    # Add namespaces for the auth and crud routes
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(item_ns, path="/item")
    api.add_namespace(user_ns, path="/user")

    return app

