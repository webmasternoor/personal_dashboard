import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin@localhost:5432/personaldashboard"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret"