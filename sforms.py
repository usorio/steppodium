from wtforms import validators, StringField,TextField, IntegerField, SelectField, ValidationError, SubmitField, PasswordField, SelectMultipleField, widgets
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField

offices = ['Austin','Mount Laurel','Radnor','Johnstown','Cherry Hill','Pittsburgh','Philadelphia','Princeton']
positions = ['Intern','Account Manager','Compliance','Consultant','Analyst','Sales','IT','Administration']


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
        email = field.data.lower()
        if email in ['lddemi@gmail.com','jmhughes018@gmail.com', 'zac.demi@gmail.com', 'dan.k.lee.0@gmail.com']:
            pass
        elif email[len(email)-4-len(company):-4] != company:
            raise ValidationError(message)
    
    return _custom_email

#email on main page
class emailOnly(FlaskForm):
    email = EmailField('Email',validators=[validators.DataRequired()]) #,custom_email('ajg')])

#if user exist then prompt for password
#email is pulled in from above
class loginUser(emailOnly):
    password = PasswordField('Password',validators=[validators.DataRequired()])

#if user does not exist then redirect to register
class registerUser(FlaskForm):
    display_name = StringField('Display Name',validators=[validators.DataRequired()])
    password = PasswordField('Enter Password',validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'Passwords must match')])
    confirm = PasswordField('Repeat Password')
    position = SelectField('Job Title',choices=tuple_list(positions))
    office = SelectField('Office',choices=tuple_list(offices))

class passwordsOnly(FlaskForm):
    password = PasswordField('Enter Password',validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'Passwords must match')])
    confirm = PasswordField('Repeat Password')

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class enterSteps(FlaskForm):
    steps_walked = IntegerField('Steps Entry', validators=[validators.NumberRange(min=0, max=50000)])

class editSteps(FlaskForm):
    edit_steps = MultiCheckboxField('edit_steps', validators=[validators.Required()])
    #def __init__(self,tagtuple):
    #    self.tagtuple = tagtuple
    #    self.edit_steps = MultiCheckboxField('edit_steps',choices=self.tagtuple,validators=[validators.Required()])
