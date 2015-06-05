from flask import render_template
from project import app, mail, client
from flask_mail import Message
from bson.objectid import ObjectId
from datetime import datetime

#define user database
db = client.steppodium
user = db.users

def sendemail(esubject, esender, erecipients, ehtml):
#    esubject = "Sample Subject"
#    esender = "jmhughes018@gmail.com"
#    erecipients = ["jmhughes018@gmail.com"]
#    ehtml = "This is the body of the email"

    msg = Message(esubject, sender = esender, recipients = erecipients)
    msg.html = ehtml

    mail.send(msg)

def sendconfirm(email, user_id):
    erecipients = list(email)
    esubject, esender, erecipients = 'You are almost registered!', 'jmhughes018@gmail.com', ['zac_demi@ajg.com', 'jmhughes018@gmail.com']
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

def update_user(_id,dname,pwd,job,office):
    user.update({"_id":ObjectId(_id)},{"$set":{"display_name":dname,
                "password":frequency,"job_title":job,"office":office}})

def add_steps(_id,steps):
    date = datetime.now()
    entry = {steps,date}
    user.update({"_id":ObjectId(_id)},{"$push":{"steps":entry}})

def return_id(email):
    user = user.find_one({"email":email})
    user_id = user["_id"]
    return user_id

