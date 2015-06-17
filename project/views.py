from flask import request, redirect, render_template, url_for, flash
from project import app,mail
from flask_mail import Message
from sforms import emailOnly, loginUser, registerUser, enterSteps
import podium


@app.route("/",methods = ['GET','POST'])
def index():
    #redirect to main page
    return redirect(url_for('welcome'))

@app.route("/welcome/",methods = ['GET','POST'])
def welcome():
    form = emailOnly()
    if form.validate_on_submit():
        email = form.email.data.lower()
        if podium.user_exists(email):
            flash("An email has already been sent to this address with registration information!")
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
        email = form.email.data.lower()
        password = form.password.data
        if not podium.user_exists(email) or not podium.valid_password(email,password):
            flash("Password or email is incorrect")
        else:
            user_id = podium.return_id(email)
            return redirect(url_for('dashboard',user_id=user_id))
    else:
        flash_errors(form)

    return render_template('login.html',form=form)

@app.route("/register/<user_id>/", methods = ['GET','POST'])
def register(user_id):
    form = registerUser()
    if form.validate_on_submit():
        dname, pwd  = form.display_name.data, form.password.data
        position, office = form.position.data, form.office.data
        #avatar = request.form.avatar.data
        podium.update_user(user_id, dname, pwd, position, office)
        return redirect(url_for('success'))
    else: 
        flash_errors(form)
    return render_template('register.html',form=form)

@app.route("/dashboard/<user_id>/", methods = ['GET', 'POST'])
def dashboard(user_id):
    form = enterSteps()
    if form.validate_on_submit():
        steps = form.steps_walked.data
        podium.add_steps(user_id, steps)
    else:
        flash_errors(form)
    return render_template('dashboard.html', form=form)

@app.route("/success/", methods = ['GET'])
def success():
    return render_template('success.html')
           
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error),'error')
