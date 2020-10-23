from src.app.tools.inputs.button_redirect import ButtonRedirect
from flask import render_template, request, session
from src.app.tools.forms import RegisterForm


class Register:

    _button_redirects = ButtonRedirect('button', {'send' : 'register/confirm'})

    def get(self):
        register_form = RegisterForm(request.form)
        return render_template('register.html', form=register_form, title='Register')

    def post(self):
        register_form = RegisterForm(request.form)
        return self._post_valid_login(register_form) if register_form.validate() \
             else self._post_invalid_login(register_form)

    def _post_valid_login(self, register_form_validated):
        session['username'] = register_form_validated.username.data
        return self._button_redirects(request.form['button'])

    def _post_invalid_login(self, invalid_register_form):
       return render_template('register.html', form=invalid_register_form, title='Register')