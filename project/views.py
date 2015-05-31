from project import app,mail
from flask_mail import Message

@app.route("/")
def index():
    msg = Message("Hello",
    sender="zac.demi@gmail.com",
    recipients=["zac.demi@gmail.com"])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    mail.send(msg)
    return "You just sent an email using Flask. Good work."


