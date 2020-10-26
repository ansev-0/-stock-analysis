from src.app.users_db.update.update_general_info import UpdateGeneralInfoDataBaseUsers
from src.app.users_db.find.find_general_info import FindGeneralInfoDataBaseUsers
from src.app.tools.session import UserSession


class RegisterConfirmed:

    _user = UserSession()
    _update_general_info = UpdateGeneralInfoDataBaseUsers()
    _find_general_info =  FindGeneralInfoDataBaseUsers()

    def __call__(self, token):
        
        if not self._user.in_session():
            self._username_to_session(token)
        # confirm user in db
        self._update_general_info.update_confirmed(token)
        # redirect to main
        return self._user.redirect_user_to_index()

    def _username_to_session(self, token):
        username = self._find_general_info.find_by_token_confirmed(token)['username']
        self._user.set_user(username)


        