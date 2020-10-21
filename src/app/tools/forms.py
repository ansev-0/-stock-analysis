from wtforms import Form
from wtforms import StringField, TextField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import HiddenField

class LoginForm(Form):
    username = StringField('username', 
                           [
                            validators.Required(message='El username es requerido'),
                            validators.length(min=8, max=32, message='Ingrese un username válido!.'),
                            ]
                           )
    
    password = PasswordField('password', [
                        validators.Required(message='El  password es requerido'),
                        ])