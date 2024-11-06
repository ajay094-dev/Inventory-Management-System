from flask import Flask, request, session, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session encryption

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rootuser'
app.config['MYSQL_DB'] = 'inventory_management'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/')
def home():
    return "Hello, Flask!"

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({"error": "All fields are required"}), 400

    password_hash = generate_password_hash(password)

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)', (username, password_hash, email))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "User registered successfully"}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({"message": "Logged in successfully"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# User Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

# Create Inventory Item
@app.route('/inventory', methods=['POST'])
def create_item():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    data = request.get_json()
    item_name = data.get('item_name')
    description = data.get('description')
    quantity = data.get('quantity')
    price = data.get('price')

    if not item_name or quantity is None or price is None:
        return jsonify({"error": "Item name, quantity, and price are required"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        'INSERT INTO inventory (user_id, item_name, description, quantity, price) VALUES (%s, %s, %s, %s, %s)',
        (session['user_id'], item_name, description, quantity, price)
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Inventory item created successfully"}), 201

# Read Inventory Items
@app.route('/inventory', methods=['GET'])
def read_items():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM inventory WHERE user_id = %s', (session['user_id'],))
    items = cursor.fetchall()
    cursor.close()

    return jsonify(items), 200

# Update Inventory Item
@app.route('/inventory/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    data = request.get_json()
    item_name = data.get('item_name')
    description = data.get('description')
    quantity = data.get('quantity')
    price = data.get('price')

    cursor = mysql.connection.cursor()
    cursor.execute(
        'UPDATE inventory SET item_name = %s, description = %s, quantity = %s, price = %s WHERE id = %s AND user_id = %s',
        (item_name, description, quantity, price, item_id, session['user_id'])
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Inventory item updated successfully"}), 200

# Delete Inventory Item
@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM inventory WHERE id = %s AND user_id = %s', (item_id, session['user_id']))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Inventory item deleted successfully"}), 200