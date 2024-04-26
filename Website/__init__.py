from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()  # Initialize SQLAlchemy to use for our database operations.
DB_NAME = 'database.db'  # Define the database name.

def create_app():
    app = Flask(__name__)  # Create an instance of the Flask app.
    app.config['SECRET_KEY'] = 'JEELER'  # Set a secret key for security purposes. I never use this just good principles
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Database URL for SQLAlchemy.
    db.init_app(app)  # Initialize SQLAlchemy with the Flask app.

    # Import views and auth modules that contain our routes.
    from .veiws import views
    from .auth import auth

    # Register blueprints. Blueprints organize our app into components.
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import User and Meal models for database use.
    from .models import User, Meal

    create_database(app)  # Create the database if it doesn't exist.
    
    # Initialize Flask-Login to handle user sessions.
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Redirect to login page if not logged in.
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # This callback is used by Flask-Login to load a user from an ID.
        return User.query.get(int(id))
    
    migrate = Migrate(app, db)  # Initialize Flask-Migrate for database migrations. (HERE IF I NEED TO MOVE THE DATABASE OR LOOK AT IT NOT IMPORTANT)
    return app

def create_database(app):
    # Function to create a new database if it doesn't already exist.
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()  # Create all tables in the database.
        print('Created Database!')
