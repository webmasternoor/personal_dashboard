from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ---------------- USER ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))

# ---------------- PROFILE ----------------
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bio = db.Column(db.String(500))
    age = db.Column(db.Integer)

# ---------------- SETTINGS ----------------
class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    theme = db.Column(db.String(50))
    notifications_enabled = db.Column(db.Boolean, default=True)

# ---------------- NOTIFICATIONS ----------------
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    message = db.Column(db.String(255))

# ---------------- FRIENDS ----------------
class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    friend_id = db.Column(db.Integer)