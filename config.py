import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_secreta_predeterminada')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:sqlnicolas21@localhost/parcialagro'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True