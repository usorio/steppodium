from project import app, mail
from flask import render_template
from flask_mail import Message

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
