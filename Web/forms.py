from wtforms import StringField, PasswordField, BooleanField,\
    SubmitField, EmailField, TextAreaField, FileField, HiddenField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm, RecaptchaField


class LoginForm(FlaskForm):
    email = StringField('Mail or username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Enter')


class RegisterForm(FlaskForm):
    email = EmailField('Mail address', validators=[DataRequired()])
    login = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Password again', validators=[DataRequired()])
    about = TextAreaField("About you")
    picture = FileField()
    recaptcha = RecaptchaField()
    submit = SubmitField('Confirm')


class SearchForm(FlaskForm):
    search = StringField(render_kw={"placeholder": "Search.."})
    submit = HiddenField(SubmitField)
