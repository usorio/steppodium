from wtforms import validators, StringField,TextField, IntegerField, SelectField, SelectMultipleField, SubmitField, PasswordField
from flask_wtf import Form
from wtforms.fields.html5 import EmailField

offices = ['Radnor','Johnstown','Cherry Hill','Pittsburgh','Philadelphia','Princeton']
positions = ['Senior Consultant','Consultant','Analyst','Sales','Employee Advocate']

#custom validator that requires company email
def custom_email(company):
    message = 'Email must be an ' + company + ' email address'

    def _custom_email(form,field):
        email = field.data
        if email != "zac_demi@AJG.com":
        #if email[len(email)-3-len(company):-3] != company:
            raise ValidationError(message)
    
    return _custom_email

#email on main page
class emailOnly(Form):
    email = EmailField('Company Email',[custom_email('AJG')])

#if user exist then prompt for password
#email is pulled in from above
class login(emailOnly):
    password = PasswordField('Enter Password',[validators.DataRequired])

#if user does not exist then redirect to register
class register(Form):
    display_name = StringField('Display name')
    password = PasswordField('Enter Password',[
        validators.DataRequired,
        validators.EqualTo('confrim', message = 'Passwords must match')])
    confirm = PasswordField('Repeat Password')
    position = SelectField('Job Title',choices=[positions.sort()])
    office = SelectField('Office',choices=[offices.sort()])
    
