from datetime import datetime

from flask_wtf import FlaskForm
import sqlalchemy as sa
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
#from wtforms.validators import Email # requires email-validator to be installed

from .extensions import db
from .models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    #email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self,
                          username):  # Custom validator to prevent duplicate usernames
        user = db.session.scalar(
            sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    ##### Optional email field. Requires Email validator.   # def validate_email(self, email):   #     user = db.session.scalar(sa.select(User).where(  #         User.email == email.data))  #     if user is not None:  #         raise ValidationError('Please use a different email address.')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', render_kw=dict(readonly=True))
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Update Profile')


class DeleteUserForm(FlaskForm):
    user = SelectField('User', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Delete Account')


class CheckoutForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    card_type = SelectField('Card Type',
                            choices=[('visa', 'Visa'), ('mc', 'Mastercard'),
                                     ('amex', 'American Express'),
                                     ('disc', 'Discover')],
                            validators=[DataRequired()])
    card_number = StringField('Card Number', validators=[DataRequired(),
                                                         Length(min=16,
                                                                max=16)])
    months = [(str(i), str(i)) for i in range(1, 13)]
    years = [(str(i), str(i)) for i in range(2024, 2034)]
    exp_month = SelectField("Expiration Month", choices=months,
                            validators=[DataRequired()])
    exp_year = SelectField("Expiration Year", choices=years,
                           validators=[DataRequired()])
    cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=3)])
    submit = SubmitField('Submit Order')

    def validate_exp_month(self, exp_month):
        """Validate the expiration date has not passed."""
        # Expired earlier this year.
        if (int(self.exp_year.data) <= datetime.now().year and
                int(exp_month.data) < datetime.now().month):
            raise ValidationError('Card has expired')
        # Expired a previous year.
        if int(self.exp_year.data) < datetime.now().year:
            raise ValidationError('Card has expired')
