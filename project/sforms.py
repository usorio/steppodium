from wtforms import validators, StringField,TextField, IntegerField, SelectField, ValidationError, SubmitField, PasswordField
from flask_wtf import Form
from wtforms.fields.html5 import EmailField

offices = ['Radnor','Johnstown','Cherry Hill','Pittsburgh','Philadelphia','Princeton']
positions = ['Senior Consultant','Consultant','Analyst','Sales','Employee Advocate']

#convert new_list into new_tuples
def tuple_list(new_list):
    new_tuple = []
    for x in new_list:
        insert = (x,x)
        new_tuple.append(insert)

    new_tuple = sorted(new_tuple)
    return new_tuple

#custom validator that requires company email
def custom_email(company):
    message = 'Email must be an ' + company + ' email address'

    def _custom_email(form,field):
        email = field.data
        if email[len(email)-4-len(company):-4] != company:
            raise ValidationError(message)
    
    return _custom_email

#email on main page
class emailOnly(Form):
    email = EmailField('Company Email',validators=[validators.DataRequired(),custom_email('AJG')])

#if user exist then prompt for password
#email is pulled in from above
class login(emailOnly):
    password = PasswordField('Enter Password',[validators.DataRequired])

#if user does not exist then redirect to register
class registerUser(Form):
    display_name = StringField('Display name')
    password = PasswordField('Enter Password',validators=[
        validators.DataRequired,
        validators.EqualTo('confirm', message = 'Passwords must match')])
    confirm = PasswordField('Repeat Password')
    position = SelectField('Job Title',choices=tuple_list(positions))
    office = SelectField('Office',choices=tuple_list(offices))
    
