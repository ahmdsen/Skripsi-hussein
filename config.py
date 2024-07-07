import os

class Config:
    SECRET_KEY = 'sJpufMj1em'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/bansosdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
