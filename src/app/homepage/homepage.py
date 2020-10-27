from flask import render_template, request, redirect, url_for
from src.app.tools.session import UserSession
from src.app.app import app
from src.app.tools.inputs.button_redirect import ButtonRedirect

class HomePage:

    _button_redirects = ButtonRedirect('button', {'sin in' : 'login',
                                                  'sin up' : 'register'})
    _user = UserSession()

    def get(self):
        return self._get_with_session() if self._user.in_session() else self._get_without_session()

    def post(self):
        return self._post_with_session() if self._user.in_session() else self._post_without_session()

    def _get_with_session(self):
        return render_template('homepage_with_session.html', title='Financialworks')

    def _get_without_session(self):
        return render_template('homepage_without_session.html', title='Financialworks')

    def _post_with_session(self):
        pass

    def _post_without_session(self):
        if 'button' in request.form:
            return self._button_redirects(request.form['button'])
        raise ValueError










