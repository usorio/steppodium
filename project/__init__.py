from flask import Flask
from flask_mail import Mail
from flask.ext.bcrypt import Bcrypt
from gmail_config import MAIL_USERNAME, MAIL_PASSWORD, SECRET_KEY
from pymongo import MongoClient

# set config mail server
DEBUG = True
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = MAIL_USERNAME
MAIL_PASSWORD = MAIL_PASSWORD
MAIL_DEFAULT_SENDER = MAIL_USERNAME
SECRET_KEY = SECRET_KEY
SERVER_NAME = '127.0.0.1:5030'

#initiate application
app = Flask(__name__)

#initiate config
app.config.from_object(__name__)

#initialize mail: note after config set
mail = Mail(app)

#initiate MONGODB
client = MongoClient()

#initiate Bcrypt for passwords
bcrypt = Bcrypt(app)

#initialize views
from project import views


