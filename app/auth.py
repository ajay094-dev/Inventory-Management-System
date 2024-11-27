from flask import Blueprint, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import execute_query, fetch_query
import re

auth_bp = Blueprint('auth', __name__)

def validate_username(username):
    """Validate the username: at least 6 characters, alphanumeric only."""
    if len(username) < 6:
        return "Username must be at least 6 characters long."
    if not username.isalnum():
        return "Username must contain only alphanumeric characters."
    return None

def validate_password(password):
    """Validate the password: at least 8 characters, with one uppercase, one lowercase, and one digit."""
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return "Password must contain at least one lowercase letter."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit."
    return None

def validate_email(email):
    """Validate the email address format."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return "Invalid email address."
    return None

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Validate username
    username_error = validate_username(username)
    if username_error:
        return jsonify({"error": username_error}), 400

    # Validate password
    password_error = validate_password(password)
    if password_error:
        return jsonify({"error": password_error}), 400

    # Validate email
    email_error = validate_email(email)
    if email_error:
        return jsonify({"error": email_error}), 400

    # Check if email or username already exists
    existing_user = fetch_query('SELECT * FROM users WHERE username = %s OR email = %s', (username, email))
    if existing_user:
        return jsonify({"error": "Username or email already exists."}), 409

    # Hash the password and save the user
    password_hash = generate_password_hash(password)
    execute_query('INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)', (username, password_hash, email))

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = fetch_query('SELECT * FROM users WHERE username = %s', (username,))
    if user and check_password_hash(user[0]['password_hash'], password):
        session['user_id'] = user[0]['id']
        session['username'] = user[0]['username']
        return jsonify({"message": "Logged in successfully"}), 200

    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200