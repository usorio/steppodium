from flask import request, redirect, render_template, url_for
from project import app,mail
from flask_mail import Message
from sforms import emailOnly, login, register


@app.route("/",methods = ['GET','POST'])
def welcome():
    form = emailOnly()
    if request.method == 'POST' and form.validate:
        return "Success!"
    else:
        flash_errors(form)

    return render_template('welcome.html',form=form)
    
@app.route("/login")
def login():
    form = login()


@app.route("/register")
def register():
    form = register()

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error),'error')
