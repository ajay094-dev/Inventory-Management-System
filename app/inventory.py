from flask import Blueprint, request, session, jsonify
from .models import execute_query, fetch_query

inventory_bp = Blueprint('inventory', __name__)

def validate_item_name(item_name):
    """Validate the item name: must be a non-empty string."""
    if not item_name or not isinstance(item_name, str) or len(item_name.strip()) == 0:
        return "Item name must be a non-empty string."
    if len(item_name) > 100:
        return "Item name must not exceed 100 characters."
    return None

def validate_description(description):
    """Validate the description: optional but must not exceed 500 characters."""
    if description and len(description) > 500:
        return "Description must not exceed 500 characters."
    return None

def validate_quantity(quantity):
    """Validate the quantity: must be a positive integer."""
    if quantity is None or not isinstance(quantity, int) or quantity < 0:
        return "Quantity must be a non-negative integer."
    return None

def validate_price(price):
    """Validate the price: must be a non-negative float."""
    if price is None or not isinstance(price, (int, float)) or price < 0:
        return "Price must be a non-negative number."
    return None




@inventory_bp.route('/inventory', methods=['POST'])
def create_item():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    data = request.get_json()
    item_name = data.get('item_name')
    description = data.get('description', '')  # Default to empty string if not provided
    quantity = data.get('quantity')
    price = data.get('price')

    # Validate item name
    item_name_error = validate_item_name(item_name)
    if item_name_error:
        return jsonify({"error": item_name_error}), 400

    # Validate description
    description_error = validate_description(description)
    if description_error:
        return jsonify({"error": description_error}), 400

    # Validate quantity
    quantity_error = validate_quantity(quantity)
    if quantity_error:
        return jsonify({"error": quantity_error}), 400

    # Validate price
    price_error = validate_price(price)
    if price_error:
        return jsonify({"error": price_error}), 400

    # Save item to the database
    execute_query(
        'INSERT INTO inventory (user_id, item_name, description, quantity, price) VALUES (%s, %s, %s, %s, %s)',
        (session['user_id'], item_name, description, quantity, price)
    )

    return jsonify({"message": "Inventory item created successfully"}), 201



@inventory_bp.route('/inventory', methods=['GET'])
def read_items():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    items = fetch_query('SELECT * FROM inventory WHERE user_id = %s', (session['user_id'],))
    return jsonify(items), 200



@inventory_bp.route('/inventory/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    data = request.get_json()
    item_name = data.get('item_name')
    description = data.get('description', '')  # Default to empty string if not provided
    quantity = data.get('quantity')
    price = data.get('price')

    # Validate item name
    item_name_error = validate_item_name(item_name)
    if item_name_error:
        return jsonify({"error": item_name_error}), 400

    # Validate description
    description_error = validate_description(description)
    if description_error:
        return jsonify({"error": description_error}), 400

    # Validate quantity
    quantity_error = validate_quantity(quantity)
    if quantity_error:
        return jsonify({"error": quantity_error}), 400

    # Validate price
    price_error = validate_price(price)
    if price_error:
        return jsonify({"error": price_error}), 400

    # Update item in the database
    execute_query(
        'UPDATE inventory SET item_name = %s, description = %s, quantity = %s, price = %s WHERE id = %s AND user_id = %s',
        (item_name, description, quantity, price, item_id, session['user_id'])
    )

    return jsonify({"message": "Inventory item updated successfully"}), 200




@inventory_bp.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    execute_query('DELETE FROM inventory WHERE id = %s AND user_id = %s', (item_id, session['user_id']))
    return jsonify({"message": "Inventory item deleted successfully"}), 200