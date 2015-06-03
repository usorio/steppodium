from flask import request, redirect, render_template, url_for, flash
from project import app,mail
from flask_mail import Message
from sforms import emailOnly, login, registerUser


@app.route("/",methods = ['GET','POST'])
def welcome():
    form = emailOnly()
    if form.validate_on_submit():
        return "Success!"
    else:
        flash_errors(form)

    return render_template('welcome.html',form=form)
    
@app.route("/login")
def login():
    form = login()
    pass


@app.route("/register", methods = ['GET','POST'])
def register():
    form = registerUser()
    if form.validate_on_submit():
        return "Success!"
    else: 
        flash_errors(form)
    return render_template('register.html',form=form)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error),'error')
