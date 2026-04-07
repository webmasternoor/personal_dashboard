# backend_mongodb/routes/users.py
from flask import Blueprint, request, jsonify, current_app # Import current_app
from bson import ObjectId # Import ObjectId for MongoDB
from werkzeug.security import generate_password_hash # For password hashing
from datetime import datetime # Import datetime

# Removed SQLAlchemy imports:
# from models import db, User, Profile, Settings

users_bp = Blueprint('users', __name__, url_prefix='/users') # Added url_prefix for consistency

# Helper to convert MongoDB ObjectId to string for JSON serialization
def serialize_user(user_doc):
    if user_doc and '_id' in user_doc:
        # Convert ObjectId to string for JSON compatibility
        user_doc['_id'] = str(user_doc['_id'])
    return user_doc

# 1. Create user (POST /users)
@users_bp.route('/', methods=['POST']) # Route now matches blueprint prefix
def create_user_route():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing username, email, or password"}), 400

    # Access mongo client via current_app
    mongo_client = current_app.extensions['pymongo']

    # Check if user already exists (case-insensitive for username/email)
    existing_user = mongo_client.db.users.find_one({
        "$or": [
            {"username": data["username"].lower()},
            {"email": data["email"].lower()}
        ]
    })
    if existing_user:
        return jsonify({"error": "Username or email already exists"}), 400

    try:
        hashed_password = generate_password_hash(data["password"])
        user_data = {
            "username": data["username"],
            "email": data["email"],
            "password": hashed_password,
            "status": "Active", # Default status
            "created_at": datetime.utcnow(), # Manual timestamp
            "updated_at": datetime.utcnow()  # Manual timestamp
        }
        # Insert the new user document
        result = mongo_client.db.users.insert_one(user_data)
        new_user_id = result.inserted_id

        # Fetch the created user to return it (optional, but good practice)
        created_user = mongo_client.db.users.find_one({"_id": new_user_id})

        return jsonify(serialize_user(created_user)), 201 # Return created user with string ID

    except Exception as e:
        print(f"ERROR creating user: {e}")
        return jsonify({"error": "Failed to create user", "message": str(e)}), 500

# 2. Get all users (GET /users)
@users_bp.route('/', methods=['GET']) # Route now matches blueprint prefix
def get_all_users_route():
    # Access mongo client via current_app
    mongo_client = current_app.extensions['pymongo']
    try:
        # Fetch all users from the 'users' collection
        users = list(mongo_client.db.users.find())
        # Serialize ObjectIds to strings for JSON response
        serialized_users = [serialize_user(user) for user in users]
        return jsonify(serialized_users), 200
    except Exception as e:
        print(f"ERROR fetching users: {e}")
        return jsonify({"error": "Failed to fetch users", "message": str(e)}), 500

# 3. Get user by ID (GET /users/<id>) - Note: MongoDB uses string IDs or ObjectIds
@users_bp.route('/<string:user_id_str>', methods=['GET']) # Use string for ID
def get_user_by_id_route(user_id_str):
    try:
        # Access mongo client via current_app
        mongo_client = current_app.extensions['pymongo']

        # Convert string ID to ObjectId
        user_id = ObjectId(user_id_str)
    except Exception:
        return jsonify({"error": "Invalid user ID format"}), 400

    user = mongo_client.db.users.find_one({"_id": user_id})

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(serialize_user(user)), 200

# 4. Update user (PUT /users/<id>)
@users_bp.route('/<string:user_id_str>', methods=['PUT']) # Use string for ID
def update_user_route(user_id_str):
    try:
        # Access mongo client via current_app
        mongo_client = current_app.extensions['pymongo']
        user_id = ObjectId(user_id_str)
    except Exception:
        return jsonify({"error": "Invalid user ID format"}), 400

    user = mongo_client.db.users.find_one({"_id": user_id})
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    # Prepare update data - only include fields that are present in the request
    update_fields = {}
    if "username" in data:
        update_fields["username"] = data["username"]
    if "email" in data:
        update_fields["email"] = data["email"]
    # Add other updatable fields here if necessary

    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400

    # Add updated_at timestamp
    update_fields["updated_at"] = datetime.utcnow()

    # Perform the update
    result = mongo_client.db.users.update_one(
        {"_id": user_id},
        {"$set": update_fields}
    )

    if result.modified_count == 1:
        # Fetch the updated user to return
        updated_user = mongo_client.db.users.find_one({"_id": user_id})
        return jsonify(serialize_user(updated_user)), 200
    else:
        # This could happen if the data provided was the same as existing data,
        # or if the update somehow failed without raising an exception.
        return jsonify({"error": "User not updated", "message": "No changes were made or an unknown error occurred."}), 500


# 5. Delete user (DELETE /users/<id>)
@users_bp.route('/<string:user_id_str>', methods=['DELETE']) # Use string for ID
def delete_user_route(user_id_str):
    try:
        # Access mongo client via current_app
        mongo_client = current_app.extensions['pymongo']
        user_id = ObjectId(user_id_str)
    except Exception:
        return jsonify({"error": "Invalid user ID format"}), 400

    # Perform the deletion
    result = mongo_client.db.users.delete_one({"_id": user_id})

    if result.deleted_count == 1:
        return jsonify({"msg": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found or could not be deleted"}), 404