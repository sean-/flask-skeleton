from flaskext.wtf import BooleanField, Email, EqualTo, Form, Length, \
    Required, PasswordField, SubmitField, TextField, ValidationError

USERNAME = 'user@example.com'
PASSWORD = 'admin'

class LoginForm(Form):
    email = TextField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField("Login")

    def validate_email(self, field):
        if field.data != USERNAME:
            raise ValidationError, "Invalid username"

    def validate_password(self, field):
        if field.data != PASSWORD:
            raise ValidationError, "Invalid password"


class RegisterForm(Form):
    email = TextField('Email Address', validators = [Email()])
    password = PasswordField('New Password', validators = [
            Required(),
            Length(min=8, max=80),
            EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', validators = [Required()])
    submit = SubmitField("Register")
