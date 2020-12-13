from flask import redirect, url_for, request

class ButtonRedirect:

    def __init__(self, name_button, dict_redirects):
        self._name_button = name_button
        self._dict_redirects = dict_redirects


    @property
    def name_button(self):
        return self._name_button

    @property
    def dict_redirects(self):
        return self._dict_redirects


    def __call__(self, key):
        where = self._dict_redirects[key]
        return self._redirect_with_url_for(where) if where != '' else self._redirect_base()


    def _redirect_with_url_for(self, where):
        redirect_to = url_for(where)
        return redirect(redirect_to)


    def _redirect_base(self):

        return redirect('/')


    