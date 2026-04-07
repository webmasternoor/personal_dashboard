# backend_mongodb/models.py

# Removed SQLAlchemy imports and initialization
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime, timezone
# db = SQLAlchemy()

# Import ObjectId for MongoDB's default _id type
from bson import ObjectId
# Import datetime for timestamps
from datetime import datetime

# Note: Flask-PyMongo integrates with the app context.
# The 'mongo' object will be available in routes via current_app.extensions['pymongo'].

# We are removing the SQLAlchemy models. MongoDB is schema-less by default,
# and interactions are usually done via dictionaries or Flask-PyMongo's document helpers.
# The User model definition is now effectively handled within the routes.

# Example placeholder if you need a Python object representation (optional):
# This class is NOT directly used by Flask-PyMongo for DB operations but can help structure data.
class User:
    def __init__(self, username, email, password, _id=None):
        self.username = username
        self.email = email
        self.password = password
        self._id = _id # MongoDB's ObjectId

    def to_dict(self):
        # Convert to dictionary for MongoDB insertion
        data = {
            "username": self.username,
            "email": self.email,
            "password": self.password, # Store hashed password
            "status": "Active", # Default status
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        if self._id:
            data["_id"] = self._id
        return data

    @staticmethod
    def from_dict(data):
        # Create User object from MongoDB document
        return User(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"), # This would be the hashed password
            _id=data.get("_id")
        )
# In your routes, you'll likely use dictionaries directly with mongo_client.db.users.