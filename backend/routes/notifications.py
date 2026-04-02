from flask import Blueprint, request, jsonify
from models import db, Notification

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/users/<int:id>/notifications', methods=['GET'])
def get_notifications(id):
    data = Notification.query.filter_by(user_id=id).all()
    return jsonify([n.message for n in data])

@notifications_bp.route('/users/<int:id>/notifications', methods=['POST'])
def create_notification(id):
    data = request.json
    notif = Notification(user_id=id, message=data['message'])
    db.session.add(notif)
    db.session.commit()
    return jsonify({"msg": "Created"})

@notifications_bp.route('/users/<int:id>/notifications/<int:nid>', methods=['GET'])
def get_notification(id, nid):
    n = Notification.query.get(nid)
    return jsonify({"message": n.message})

@notifications_bp.route('/users/<int:id>/notifications/<int:nid>', methods=['PUT'])
def update_notification(id, nid):
    n = Notification.query.get(nid)
    n.message = request.json['message']
    db.session.commit()
    return jsonify({"msg": "Updated"})

@notifications_bp.route('/users/<int:id>/notifications/<int:nid>', methods=['DELETE'])
def delete_notification(id, nid):
    n = Notification.query.get(nid)
    db.session.delete(n)
    db.session.commit()
    return jsonify({"msg": "Deleted"})