from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm, RecaptchaField


class LoginForm(FlaskForm):
    email = StringField('Никнейм или почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    login = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    about = TextAreaField("О себе")
    recaptcha = RecaptchaField()
    submit = SubmitField('Зарегистрироваться')
