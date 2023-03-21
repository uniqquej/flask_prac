from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    user_id = StringField('user_Id', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(LoginForm):
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo(
            'repassword',
            message='password must match!!'
        )
    ])
    repassword = PasswordField('Confirm Password', validators=[
        DataRequired()
    ])
    
    username = StringField('username', validators=[DataRequired()])