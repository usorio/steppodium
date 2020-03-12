import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_pymongo import PyMongo

#initiate application
app = Flask(__name__)
app.config.from_pyfile("config/config.py")

#initialize mail: note after config set
mail = Mail(app)

#initiate MONGODB
mongo = PyMongo(app)

#initiate Bcrypt for passwords
bcrypt = Bcrypt(app)

from . import routes