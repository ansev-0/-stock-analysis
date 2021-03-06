from src.app.tools.before_request.abstract_before_request_task import BeforeRequestTask
from src.app.tools.session import UserSession
from flask import session
from datetime import timedelta


class RedirectNotUserInSessionTask(BeforeRequestTask):

    _user = UserSession()

    def __init__(self, endpoints_task):
        super().__init__(endpoints_task)

    def __call__(self):
        if self.endpoint_in_endpoints_task and not self._user.in_session():
            self._user.redirect_user_to_login()


class ModifiedSessionTask(BeforeRequestTask):
    
    def __init__(self):
        super().__init__(None)

    def __call__(self, app):
        session.modified = True

