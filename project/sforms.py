from wtforms import validators, StringField,TextField, IntegerField, SelectField, ValidationError, SubmitField, PasswordField, SelectMultipleField
from flask_wtf import Form
from wtforms.fields.html5 import EmailField

offices = ['Mount Laurel','Radnor','Johnstown','Cherry Hill','Pittsburgh','Philadelphia','Princeton']
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
class emailOnly(Form):
    email = EmailField('Company Email',validators=[validators.DataRequired(),custom_email('ajg')])

#if user exist then prompt for password
#email is pulled in from above
class loginUser(emailOnly):
    password = PasswordField('Enter Password',validators=[validators.DataRequired()])

#if user does not exist then redirect to register
class registerUser(Form):
    display_name = StringField('Display Name',validators=[validators.DataRequired()])
    password = PasswordField('Enter Password',validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'Passwords must match')])
    confirm = PasswordField('Repeat Password')
    position = SelectField('Job Title',choices=tuple_list(positions))
    office = SelectField('Office',choices=tuple_list(offices))

class passwordsOnly(Form):
    password = PasswordField('Enter Password',validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'Passwords must match')])
    confirm = PasswordField('Repeat Password')

# class MultiCheckboxField(SelectMultipleField):
#    """
#    A multiple-select, except displays a list of checkboxes.
#
#    Iterating the field will produce subfields, allowing custom rendering of
#    the enclosed checkbox fields.
#    """
#    widget = widgets.ListWidget(prefix_label=False)
#    option_widget = widgets.CheckboxInput()

class enterSteps(Form):
    steps_walked = IntegerField('Steps Entry', validators=[validators.NumberRange(min=0, max=50000)])
    # taglist = MultiCheckboxField('Tags',choices=tagtuple,validators=[validators.Required()])
