import os

class Config:
    SECRET_KEY = 'd2b0873fb7c652daa2ccc52b5b479edd'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///books.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/images'