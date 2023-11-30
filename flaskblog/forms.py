from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=8)])
    confirm_password = PasswordField('Confim Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_user(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')
    

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=8)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

    # def validate_username(self, username):
    #     uname = User.query.filter_by(username=username.data).exists()
    #     if not uname:
    #         raise ValidationError('Username does not exist')
        
    # def validate_email(self, email):
    #     pwd = User.query.filter_by(password=password.data).exists()
    #     if not pwd:
    #         raise ValidationError('Incorrect password')
                    

class UpdateAccountForms(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired()])
    image = FileField('Update Image', validators=[FileAllowed([
                        'jpeg', 'jpg', 'png', 'svg'
                    ])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(' Username already exists ')
    
    def validate_email(sself, email):
        if email.data != current_user.email:
            user_email = User.query.filter_by(email=email.data).first()
            if user_email:
                raise ValidationError(' Email already exists ')


class PublishForms(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Publish')


class Request_ResetPassword_TokenForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Send Email')
    def validate_email(self, email):
        user_email = User.query.filter_by(email=email).first()
        if not user_email:
            raise ValidationError('Email does not exist')


class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=8)])
    confirm_pwd = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')