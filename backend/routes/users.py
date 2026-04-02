from flask import Blueprint, request, jsonify
from models import db, User, Profile, Settings

users_bp = Blueprint('users', __name__)

# 1. Create user
@users_bp.route('/users', methods=['POST'])
def create_user():
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
        print("ERROR:", e)  # 👈 VERY IMPORTANT (check terminal)
        return jsonify({"error": str(e)}), 500

# 2. Get all users
@users_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.username for u in users])

# 3. Get user by ID
@users_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return jsonify({"username": user.username})

# 4. Update user
@users_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    data = request.json
    user.username = data.get("username", user.username)
    db.session.commit()
    return jsonify({"msg": "Updated"})

# 5. Delete user
@users_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "Deleted"})

# 6. Login
@users_bp.route('/users/login', methods=['POST'])
def login():
    return jsonify({"msg": "Login success"})

# 7. Logout
@users_bp.route('/users/logout', methods=['POST'])
def logout():
    return jsonify({"msg": "Logout success"})

# 8. Get profile
@users_bp.route('/users/<int:id>/profile', methods=['GET'])
def get_profile(id):
    profile = Profile.query.filter_by(user_id=id).first()
    return jsonify({"bio": profile.bio})

# 9. Update profile
@users_bp.route('/users/<int:id>/profile', methods=['PUT'])
def update_profile(id):
    profile = Profile.query.filter_by(user_id=id).first()
    data = request.json
    profile.bio = data.get("bio", profile.bio)
    db.session.commit()
    return jsonify({"msg": "Profile updated"})

# 10. Get settings
@users_bp.route('/users/<int:id>/settings', methods=['GET'])
def get_settings(id):
    settings = Settings.query.filter_by(user_id=id).first()
    return jsonify({"theme": settings.theme})

# 11. Update settings
@users_bp.route('/users/<int:id>/settings', methods=['PUT'])
def update_settings(id):
    settings = Settings.query.filter_by(user_id=id).first()
    data = request.json
    settings.theme = data.get("theme", settings.theme)
    db.session.commit()
    return jsonify({"msg": "Settings updated"})