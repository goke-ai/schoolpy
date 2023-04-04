from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, validators
from wtforms.validators import Length, DataRequired, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=25)])
    email = StringField('Email Address', validators=[Length(min=6, max=35)])
    password = PasswordField('New Password', validators=[DataRequired(),
                                                         EqualTo(
                                                             'confirm', message='Passwords must match')
                                                         ])
    confirm = PasswordField('Repeat Password')
    # accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    submit = SubmitField('Register')
