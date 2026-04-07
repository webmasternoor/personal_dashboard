# backend_mongodb/app.py
from flask import Flask
from config import Config
# Removed: from models import db # No longer using SQLAlchemy db
from flask_pymongo import PyMongo # Import Flask-PyMongo

# Import blueprints
from routes.users import users_bp # Import the blueprint factory/object
# from routes.notifications import notifications_bp # Assuming these also need mongo
# from routes.friends import friends_bp # Assuming these also need mongo

from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

# --- CORS Configuration ---
# Allow requests from your frontend's origin (e.g., http://localhost:5173)
# Adjust if your frontend runs on a different port or domain
CORS(app, resources={r"/users/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
# --- End CORS Configuration ---

# Initialize Flask-PyMongo
mongo = PyMongo(app)

# Register blueprints
app.register_blueprint(users_bp)

if __name__ == "__main__":
    # MongoDB does not use db.create_all()
    # If you need to create indexes, do it here using mongo.db.<collection>.create_index()
    with app.app_context():
        try:
            # Example: Ensure 'users' collection exists and has indexes
            # Check if indexes already exist before creating to avoid errors on subsequent runs
            existing_indexes = mongo.db.users.index_information()
            if 'email_1' not in existing_indexes:
                mongo.db.users.create_index("email", unique=True)
                print("Created index on 'email' for users collection.")
            if 'username_1' not in existing_indexes:
                mongo.db.users.create_index("username", unique=True)
                print("Created index on 'username' for users collection.")
            print("Indexes for users collection are up-to-date.")
        except Exception as e:
            print(f"Error ensuring indexes for users collection: {e}")

    # Run the app on the specified port
    app.run(debug=True, port=5001) # Changed port back to 5001 as in original