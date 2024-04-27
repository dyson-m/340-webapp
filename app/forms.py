from flask_wtf import FlaskForm
import sqlalchemy as sa
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo ,Regexp, Email
from wtforms.fields.choices import SelectField

from .extensions import db
from .models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('ZIP Code', validators=[DataRequired(), Regexp('^\d{5}$', message="Enter a valid 5-digit ZIP Code")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username): # Custom validator to prevent duplicate usernames
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    ##### Optional email field. Requires Email validator. 
    # def validate_email(self, email): 
    #     user = db.session.scalar(sa.select(User).where(
    #         User.email == email.data))
    #     if user is not None:
    #         raise ValidationError('Please use a different email address.')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', render_kw=dict(readonly=True))
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Update Profile')


class DeleteUserForm(FlaskForm):
    user = SelectField('User', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Delete Account')
