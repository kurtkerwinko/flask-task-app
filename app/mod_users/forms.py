# Import Form and RecaptchaField (optional)
from flask_wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, validators # BooleanField

# Define the login form (WTForms)
class LoginForm(Form):
  username = TextField('Username', [validators.InputRequired()])
  password = PasswordField('Password', [validators.InputRequired()])

class SignUpForm(Form):
  first_name = TextField('First Name', [validators.InputRequired()])
  last_name = TextField('Last Name', [validators.InputRequired()])
  username = TextField('Username', [validators.InputRequired(), validators.Length(min=6), validators.Regexp(r'^[\w.@+-]+$', message='alphanumeric characters only')])
  password = PasswordField('Password', [validators.InputRequired(), validators.Length(min=6)])
