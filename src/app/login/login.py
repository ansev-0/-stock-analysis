from src.app.tools.inputs.button_redirect import ButtonRedirect
from flask import render_template, request, session
from src.app.tools.forms import LoginForm


class Login:

    _button_redirects = ButtonRedirect('button', {'send' : ''})

    def get(self):
        login_form = LoginForm(request.form)
        return render_template('login.html', form=login_form, title='Login')

    def post(self):
        login_form = LoginForm(request.form)
        return self._post_valid_login(login_form) if login_form.validate() \
             else self._post_invalid_login(login_form)

    def _post_valid_login(self, login_form_validated):
        session['username'] = login_form_validated.username.data
        return self._button_redirects(request.form['button'])

    def _post_invalid_login(self, invalid_login_form):
       return render_template('login.html', form=invalid_login_form, title='Login')