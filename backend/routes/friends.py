from flask import Blueprint, request, jsonify
from models import db, Friend

friends_bp = Blueprint('friends', __name__)

@friends_bp.route('/users/<int:id>/friends', methods=['GET'])
def get_friends(id):
    data = Friend.query.filter_by(user_id=id).all()
    return jsonify([f.friend_id for f in data])

@friends_bp.route('/users/<int:id>/friends', methods=['POST'])
def add_friend(id):
    data = request.json
    f = Friend(user_id=id, friend_id=data['friend_id'])
    db.session.add(f)
    db.session.commit()
    return jsonify({"msg": "Friend added"})

@friends_bp.route('/users/<int:id>/friends/<int:fid>', methods=['GET'])
def get_friend(id, fid):
    f = Friend.query.filter_by(user_id=id, friend_id=fid).first()
    return jsonify({"friend_id": f.friend_id})

@friends_bp.route('/users/<int:id>/friends/<int:fid>', methods=['DELETE'])
def delete_friend(id, fid):
    f = Friend.query.filter_by(user_id=id, friend_id=fid).first()
    db.session.delete(f)
    db.session.commit()
    return jsonify({"msg": "Deleted"})