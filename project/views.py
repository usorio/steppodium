from flask import request, redirect, render_template, url_for, flash
from project import app,mail
from flask_mail import Message
from sforms import emailOnly, loginUser, registerUser, enterSteps, passwordsOnly, editSteps
import podium
from bson.objectid import ObjectId

@app.route("/",methods = ['GET','POST'])
def index():
    #redirect to login page
    return redirect(url_for('login'))

@app.route("/welcome/",methods = ['GET','POST'])
def welcome():
    form = emailOnly()
    if form.validate_on_submit():
        email = form.email.data.lower()
        if podium.email_exists(email):
            flash("An email has already been sent to this address with registration information! Make sure to check your JUNK mailbox.")
        else:
            podium.insert_user(email)
            flash("Thanks for signing up! Check your email for a confirmation link! Email may be sent to JUNK mail.")
    else:
        flash_errors(form)

    return render_template('welcome.html',form=form)
    
@app.route("/login/", methods = ['GET','POST'])
def login():
    form = loginUser()

    if form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        if not podium.email_registered(email):
            flash("This email address is not registered")
        elif not podium.valid_password(email,password):
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
        if not podium.unique_display(user_id,"display_name",dname):
            flash("Error in Display Name Field - This display name has already been taken!")
        else:
            podium.update_user(user_id, dname, pwd, position, office)
            return redirect(url_for('success'))
    else: 
        flash_errors(form)
    return render_template('register.html',form=form)

@app.route("/dashboard/<user_id>/", methods = ['GET', 'POST'])
def dashboard(user_id):
    form = enterSteps()
    #tagtuple=podium.st2(podium.get_recent_steps(user_id))
    form2 = editSteps()

    sum_steps = podium.sum_steps(user_id)
    user = podium.return_user_object(user_id)
    individual = podium.leaderboard("$team.team_number","$avg")
    if form.validate_on_submit():
        steps = form.steps_walked.data
        podium.add_steps(user_id, steps)
        sum_steps = podium.sum_steps(user_id)
        #leaderboards
        individual = podium.leaderboard("$team.team_number","$avg")
    elif form2.validate_on_submit():
        #edit steps
        date_list = form.date_list.data
        podium.remove_steps(user_id,date_list)
    else:
        flash_errors(form)
    return render_template('dashboard.html', form=form, form2=form2, sum_steps=sum_steps, recent_steps=[],user=user,individual=individual)

@app.route("/success/", methods = ['GET'])
def success():
    return render_template('success.html')
           
@app.route("/forgot_password/", methods = ['GET','POST'])
def forgot_password():
    form = emailOnly()
    if form.validate_on_submit():
        email = form.email.data.lower()
        user_id = podium.return_id(email)
        podium.send_password_link(email,user_id)
        flash("If your email exists in our sytem, then we have sent a password reset link.")
    else:
        flash_errors(form)
 
    return render_template('forgot_password.html', form=form)
    
@app.route("/reset_password/<user_id>/", methods = ['GET','POST'])
def reset_password(user_id):
    form = passwordsOnly()
    if form.validate_on_submit():
       password = form.password.data
       podium.update_password(user_id,password)
       flash("Your password has been reset!")
    else:
       flash_errors(form)

    return render_template('reset_password.html', form=form)
 
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error),'error')
