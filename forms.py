from wtforms import Form, StringField, PasswordField, TextAreaField, validators


class LoginForm(Form):
    email = StringField('Email Address', [
        validators.DataRequired(),
        validators.Email()
    ])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])


class RegistrationForm(Form):
    email = StringField('Email Address', [
        validators.DataRequired(),
        validators.Email()
    ])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class KeyCreationForm(Form):
    tag = StringField('Key Tag', [
        validators.DataRequired()
    ])
    key = TextAreaField('Key', [
        validators.DataRequired()
    ])
