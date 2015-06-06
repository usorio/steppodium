from flask import render_template
from project import app, mail, client
from flask_mail import Message
from bson.objectid import ObjectId
from datetime import datetime
import gmail_config

#define user database
db = client.steppodium
user = db.users

def sendemail(esubject, esender, erecipients, ehtml):
    msg = Message(esubject, sender = esender, recipients = erecipients)
    msg.html = ehtml

    mail.send(msg)

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

def insert_user(email, *args):
    user.insert({"email":email,"podium_client":"ajg"})
    user_id = return_id(email)
    sendconfirm(email,user_id)

def update_user(_id,dname,pwd,position,office):
    user.update({"_id":ObjectId(_id)},{"$set":{"display_name":dname,
                "password":pwd,"position":position,"office":office}})

def add_steps(_id,steps):
    date = datetime.now()
    entry = {steps,date}
    user.update({"_id":ObjectId(_id)},{"$push":{"steps":entry}})

def return_id(email):
    user_email = user.find_one({"email":email})
    user_id = user_email["_id"]
    return user_id

