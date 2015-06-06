from flask import request, redirect, render_template, url_for, flash
from project import app,mail
from flask_mail import Message
from sforms import emailOnly, loginUser, registerUser
import podium

@app.route("/josh", methods = ['GET','POST'])
def josh():
    podium.sendconfirm()
    return "good job"

@app.route("/",methods = ['GET','POST'])
def welcome():
    form = emailOnly()
    if form.validate_on_submit():
        email = form.email.data
        if podium.user_exists(email):
            flash("You are already registered!")
        else:
            podium.insert_user(email)
            flash("Thanks for signing up! Check your email for a confirmation link!")
    else:
        flash_errors(form)

    return render_template('welcome.html',form=form)
    
@app.route("/login", methods = ['GET','POST'])
def login():
    form = loginUser()

    if form.validate_on_submit():
        return render_template('success.html')
    else:
        flash_errors(form)

    return render_template('login.html',form=form)

@app.route("/register/<user_id>/", methods = ['GET','POST'])
def register(user_id):
    form = registerUser()
    if form.validate_on_submit():
        dname, pwd  = form.display_name.data, form.password.data
        position, office = form.position.data, form.office.data
        podium.update_user(user_id, dname, pwd, position, office)
        return render_template('success.html')
    else: 
        flash_errors(form)
    return render_template('register.html',form=form)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error),'error')
