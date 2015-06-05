from flask import render_template
from project import app, mail, client
from flask_mail import Message
from bson.objectid import ObjectId
from datetime import datetime

def sendemail(esubject, esender, erecipients, ehtml):
#    esubject = "Sample Subject"
#    esender = "jmhughes018@gmail.com"
#    erecipients = ["jmhughes018@gmail.com"]
#    ehtml = "This is the body of the email"

    msg = Message(esubject, sender = esender, recipients = erecipients)
    msg.html = ehtml

    mail.send(msg)

def sendconfirm():
    esubject, esender, erecipients = 'Registration Confirmed!', 'jmhughes018@gmail.com', ['zac_demi@ajg.com', 'jmhughes018@gmail.com']
    ehtml = render_template('email-premailer.html')
    sendemail(esubject, esender, erecipients, ehtml)

#define user database
db = client.steppodium
user = db.users

def insert_user(email):
    user.insert({"email":email})

def update_user(_id,dname,pwd,job,office):
    users.update({"_id":ObjectId(_id)},{"$set":{"display_name":dname,
                "password":frequency,"job_title":job,"office":office}})

def add_steps(_id,steps):
    date = datetime.now()
    entry = {steps,date}
    users.update({"_id":ObjectId(_id)},{"$push":{"steps":entry}})

