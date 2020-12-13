from itsdangerous import SignatureExpired
from src.app.tools.inputs.button_redirect import ButtonRedirect
from flask import render_template, request, session
from src.app.tools.forms import RegisterForm
from src.app.users_db.create.create_user import CreateNewUser
from src.app.register.mail_sender import MailSender
from src.app.safe import EmailRegisterToken

class Register:

    def __init__(self, app):
        self._mail_token_sender = MailSender(app)

    _button_redirects = ButtonRedirect('button', {'send' : 'successful_register'})
    _create_new_user = CreateNewUser()
    _token = EmailRegisterToken()

    def get(self):
        register_form = RegisterForm(request.form)
        return render_template('register.html', form=register_form, title='Register')

    def post(self):
        register_form = RegisterForm(request.form)
        return self._post_valid_register(register_form) if register_form.validate() \
             else self._post_invalid_register(register_form)


    def validate_register(self, token):
        try:
            self._token.loads(token)
            return True
        except SignatureExpired:
            return False
            

    def _post_valid_register(self, register_form_validated):
        # send the email
        # get the email
        email = register_form_validated.data['email']
        # create token
        token = self._token.create(email)
        # register user in db with confirm = Token
        self._create_new_user(register_form_validated.data, token)
        # send the message
        self._mail_token_sender(email, token)
        # redirect to succes redirect, waitting to confirm
        return self._button_redirects(request.form['button'])

    def _post_invalid_register(self, invalid_register_form):
       return render_template('register.html', form=invalid_register_form, title='Register')
       