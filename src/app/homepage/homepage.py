from flask_restful import Resource
from src.app.tools.session import UserSession

class HomePage(Resource):

    _user = UserSession()

    def get(self):
        return self._get_with_session() if self._user.in_session() else self._get_without_session()

    def post(self):
        pass

    def _get_with_session(self):
        pass

    def _get_without_session(self):
        pass

    def _post_with_session(self):
        pass

    def _post_without_session(self):
        pass