from flask import Flask
from config import Config
from models import db

from routes.users import users_bp

from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db.init_app(app)

app.register_blueprint(users_bp)

if __name__ == "__main__":
    # database import for the first time 
    # with app.app_context():
    #     db.create_all()   

    # app.run(debug=True)
    app.run(debug=True, port=5001)