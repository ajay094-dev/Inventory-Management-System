from flask import Flask
from flask_mysqldb import MySQL
from flask import render_template

mysql = MySQL()

def create_app():
    """Application Factory to create Flask app"""
    app = Flask(__name__)

    # # Configuration
    # app.secret_key = 'your_secret_key'
    # app.config['MYSQL_HOST'] = 'localhost'
    # app.config['MYSQL_USER'] = 'root'
    # app.config['MYSQL_PASSWORD'] = 'rootuser'
    # app.config['MYSQL_DB'] = 'inventory_management'
    # app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    # Initialize extensions
    mysql.init_app(app)

    # Register blueprints
    from .auth import auth_bp
    from .inventory import inventory_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp)

    @app.route('/')
    def home():
        return render_template('index.html')

    return app