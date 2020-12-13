from src.app.users_db.update.update_general_info import UpdateGeneralInfoDataBaseUsers
from flask import session, redirect

class Logout:
    
    _user_db= UpdateGeneralInfoDataBaseUsers()

    def __call__(self):
        #get user from session
        username = session['username']
        self._user_db.user_logout(username)
        del session['username']
        return redirect('/')
