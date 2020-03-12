import os

DEBUG = True
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')

MONGO_URI = f"mongodb+srv://zacdemi:{os.environ.get('MONGO_PASSWORD')}@cluster0-qrc2l.mongodb.net/test?retryWrites=true&w=majority"

WTF_CSRF_SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')