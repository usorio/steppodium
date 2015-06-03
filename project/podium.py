from project import app, mail
from flask_mail import Message

def sendemail():
    esubject = "Sample Subject"
    esender = "jmhughes018@gmail.com"
    erecipients = ["jmhughes018@gmail.com"]
    ebody = "This is the body of the email"

    msg = Message(esubject, sender = esender, recipients = erecipients)
    msg.body = ebody

    mail.send(msg)
    return "You just sent an email via Flask. Pretty neat, eh?"

