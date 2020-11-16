from flask import session, redirect, url_for

class UserSession:
    
    def in_session(self):
        return 'username' in session

    def redirect_user_to_login(self):
        return redirect(url_for('login'))

    def set_user(self, user):
        session['username'] = user


    def redirect_user_to_index(self):
        return redirect('/')


    
