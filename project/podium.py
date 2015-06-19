from flask import render_template
from project import app, mail, client, bcrypt
from flask_mail import Message
from bson.objectid import ObjectId
from datetime import datetime
from decorators import async
import gmail_config

#define user database
db = client.steppodium
user = db.users


@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def sendemail(esubject, esender, erecipients, ehtml):
    msg = Message(esubject, sender = esender, recipients = erecipients)
    msg.html = ehtml
    send_async_email(app,msg)

def sendconfirm(email, user_id):
    erecipients = [email]
    esender = gmail_config.MAIL_USERNAME
    esubject = 'You are almost registered!'
    ehtml = render_template('email-premailer.html',user_id=user_id)
    sendemail(esubject, esender, erecipients, ehtml)

def user_exists(email):
    in_database = user.find({"email":email}).count()
    if in_database == 0:
        return False
    else:
        return True

def display_exists(display):
    in_database = user.find({"display_name":display}).count()
    if in_database == 0:
        return False
    else:
        return True

def valid_password(email,password):
    user_object = user.find_one({"email":email})
    pw_hash = user_object["password"]
    print pw_hash
    print password
    return bcrypt.check_password_hash(pw_hash, password)

def insert_user(email, *args):
    user.insert({"email":email,"podium_client":"ajg"})
    user_id = return_id(email)
    sendconfirm(email,user_id)

def update_user(_id,dname,password,position,office):
    #encrypt password
    password = bcrypt.generate_password_hash(password)
    user.update({"_id":ObjectId(_id)},{"$set":{"display_name":dname,
        "password":password,"position":position,"office":office}})

def add_steps(_id,steps):
    date = datetime.now()
    date = datetime.strftime(date,"%Y%m%d%H%M%S")
    entry = steps, date 
    user.update({"_id":ObjectId(_id)},{"$push":{"steps":entry}})

def return_id(email):
    user_object = user.find_one({"email":email})
    user_id = user_object["_id"]
    return user_id

