from wtforms import Form, BooleanField, TextField, PasswordField, validators, ValidationError

class RegistrationForm(Form):
    username     = TextField('Username', [validators.Length(min=4, max=25)])
    email        = TextField('Email Address', [validators.Length(min=6, max=35)])
    accept_rules = BooleanField('I accept the site rules', [validators.Required()])
    
class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')

class WeatherForm(Form):
    zipcode = TextField('ZIP Code', [validators.Regexp('^\d{5}(-\d{4})?$')])
    
form = WeatherForm()