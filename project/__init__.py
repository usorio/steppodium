from flask import Flask
from flask_mail import Mail
from gmail_config import MAIL_USERNAME, MAIL_PASSWORD

#initiate application
app = Flask(__name__)

# email server
DEBUG = True
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = MAIL_USERNAME
MAIL_PASSWORD = MAIL_PASSWORD
MAIL_DEFAULT_SENDER = MAIL_USERNAME

#set config
app.config.from_object(__name__)

#initialize mail: note after config set
mail = Mail(app)

#initialize views
from project import views

