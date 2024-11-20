import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_BINDS = {
        'budget_db': os.environ.get('DATABASE_URL')  # New database URI
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USER')
    MAIL_PASSWORD = os.environ.get('MAIL_PASS')
    PERSPECTIVE_API_KEY = os.environ.get('PERSPECTIVE_API_KEY')
    TWILLIO_ACCOUNT_SID = os.environ.get('TWILLIO_ACCOUNT_SID')
    TWILLIO_AUTH_TOKEN = os.environ.get('TWILLIO_AUTH_TOKEN')
    TWILLIO_PHONE_NUMBER = os.environ.get('WILLIO_PHONE_NUMBER')