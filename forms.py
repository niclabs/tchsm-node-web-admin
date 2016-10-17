from wtforms import Form, BooleanField, StringField, PasswordField, validators

class LoginForm(Form):
    email = StringField('Email Address', [
        validators.DataRequired(),
        validators.Email()
    ])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])

class RegistrationForm(Form):
    email = StringField('Email Address', [validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')