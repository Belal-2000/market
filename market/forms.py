from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField , PasswordField ,SubmitField
from wtforms.validators import DataRequired, Length , Email, EqualTo, ValidationError
from market.models import User


class RegesterForm(FlaskForm):
    def validate_username(self, username):
        res = User.query.filter_by(username = username.data).first()
        if res:
            raise ValidationError('Username already exist ! please try a different username')

    def validate_email(self, email):
        res = User.query.filter_by(email = email.data).first()
        if res:
            raise ValidationError('Email already exist ! please try a different username')

    username = StringField(label='User Name' , validators = [Length(min = 2 , max=30) , DataRequired()])
    email = StringField(label='Email', validators=[DataRequired() , Email()])
    password1 = PasswordField(label='password', validators=[ Length(min=6) , DataRequired()])
    password2 = PasswordField(label='Confirm password' , validators=[ EqualTo('password1','password dosn\'t match') , DataRequired()])
    submit = SubmitField(label='Create account')



class LoginForm(FlaskForm):
    username = StringField(label='User Name :' , validators = [DataRequired()])

    password = PasswordField(label='password :', validators=[ DataRequired()])

    submit = SubmitField(label='Sign in')


class Purchace(FlaskForm):
    submit = SubmitField(label='Purchace item!')

class Sell(FlaskForm):
    submit = SubmitField(label='Sell item!')
