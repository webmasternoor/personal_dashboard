# routes/users.py

from flask import Blueprint, request, jsonify
from models import db, User, Profile, Settings

users_bp = Blueprint('users', __name__)

# 1. Create user (POST /users)
@users_bp.route('/users', methods=['POST'])
def create_user_route(): # Renamed for clarity
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        user = User(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "User created"}), 201

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

# 2. Get all users (GET /users) - Returns full user details
@users_bp.route('/users', methods=['GET'])
def get_all_users_route(): # Renamed for clarity
    users = User.query.all()
    user_list = []
    for u in users:
        user_list.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "status": getattr(u, 'status', 'Active'),
            "created_at": u.created_at.isoformat() if hasattr(u, 'created_at') and u.created_at else None
        })
    return jsonify(user_list)

# --- Note: The original code had a second GET /users route that returned only usernames.
# --- This is removed as it conflicts with the above and is less useful for the frontend.
# --- If you need a different representation, create a new route or modify the above.

# 3. Get user by ID (GET /users/<int:id>)
@users_bp.route('/users/<int:id>', methods=['GET'])
def get_user_by_id_route(id): # Renamed for clarity
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    # Return more details if needed, similar to get_all_users_route
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "status": getattr(user, 'status', 'Active'),
        "created_at": user.created_at.isoformat() if hasattr(user, 'created_at') and user.created_at else None
    })

# 4. Update user (PUT /users/<int:id>)
@users_bp.route('/users/<int:id>', methods=['PUT'])
def update_user_route(id): # Renamed for clarity
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email) # Assuming email can also be updated
    # Note: Password updates usually require a different flow (e.g., change password endpoint)
    db.session.commit()
    return jsonify({"msg": "User updated"})

# 5. Delete user (DELETE /users/<int:id>)
@users_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user_route(id): # Renamed for clarity
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"})