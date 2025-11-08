from flask_wtf import FlaskForm # type: ignore
from flask_wtf.file import FileAllowed,FileRequired # type: ignore
from wtforms import StringField, TextAreaField, SubmitField, EmailField,PasswordField,FileField,SelectField,RadioField,IntegerField,MultipleFileField # type: ignore
from wtforms.validators import data_required, Email,Length # type: ignore


# ************************************************* USERS FORM ************************************************
class UserSignUpForm(FlaskForm):
    
    fname = StringField('First Name', validators=[data_required(message='You must supply your first name!')])
    lname = StringField('Last Name', validators=[data_required(message='You must supply your last name!')])
    email = EmailField('Email Address',validators=[data_required(message='You did not type any email address!'), Email(message='You email must be correct and valid!')])
    username = StringField('Username', validators=[data_required(message='You must supply your username!')])
    phone = StringField('Phone Number', validators=[data_required(message='You must supply your phone number!'), Length(min=11, max=15, message='Phone number must be between 11 and 15 characters')])
    password = PasswordField('Password:',validators=[data_required(message='Password cannot be empty!')])
    cpassword = PasswordField('Confirm Password:',validators=[data_required(message='Password cannot be empty!')])
    submit = SubmitField('Submit')

    class Meta:
        csrf=True
        csrf_time_limit=3600*2


class UserLoginForm(FlaskForm):

    username = StringField('Username/Email/Phone', validators=[data_required(message='You must supply your username or email or phone!')])
    password = PasswordField('Password',validators=[data_required(message='Password cannot be empty!')])
    submit = SubmitField('Login')

    class Meta:
        csrf=True
        csrf_time_limit=3600*2