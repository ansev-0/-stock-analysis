from wtforms import Form
from wtforms import StringField, TextField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import HiddenField
from src.app.users_db.find.find_general_info import FindGeneralInfoDataBaseUsers

class CheckLoginInDB(FindGeneralInfoDataBaseUsers):
    find_in_db = FindGeneralInfoDataBaseUsers()

    def check_username(self, form, field):
        if not self.find_in_db.exist_username_in_db(field.data):
            raise validators.ValidationError('Username not exist!')

    def check_password(self, form, field):
        if not self.find_in_db.exist_username_in_db(field.data):
            raise validators.ValidationError('Incorrect password')

class CheckRegisterInDB(FindGeneralInfoDataBaseUsers):
    find_in_db = FindGeneralInfoDataBaseUsers()

    def check_username(self, form, field):
        if self.find_in_db.exist_username_in_db(field.data):
            raise validators.ValidationError('Username already exist!')


class LoginForm(Form):

    check_login_in_db = CheckLoginInDB()

    username = StringField('username', 
                           [
                            validators.Required(message='User is required'),
                            validators.length(min=4, max=32, message='Length of username is in range 4 to 32'),
                            check_login_in_db.check_username,
                            ]
                           )
    
    password = PasswordField('password', [
                        validators.Required(message='Password is required'),
                        check_login_in_db.check_password
                        ])

class RegisterForm(Form):

    check_register_in_db = CheckRegisterInDB()

    username = StringField('username', 
                           [
                            validators.Required(message='User is required'),
                            validators.length(min=4, max=32, message='Length of username is in range 4 to 32'),
                            check_register_in_db.check_username,
                            ]
                           )
    
    password = PasswordField('password', [
                        validators.Required(message='Password is required'),
                        ])

    email = EmailField('email', [
                                 validators.Required('Email is required'),
                                 validators.Email('Enter a valid email'),
                                ])

    phone_number = StringField('phone_number')


    
