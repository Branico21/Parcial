import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_secreta_predeterminada')
    SQLALCHEMY_DATABASE_URI = 'postgresql://parcialagro_user:LMwNYqcp3Tae3HwZrH7wgELuiFoD1lQx@dpg-cvtd0vqdbo4c73cnro4g-a.oregon-postgres.render.com/parcialagro'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True