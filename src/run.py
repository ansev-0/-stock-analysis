from src.app.app import app
from src.app.homepage.homepage import HomePage
from src.app.login.login import Login
from src.app.register.register import Register

from flask import request


homepage_agent = HomePage()
login_agent = Login()
register_agent = Register()

@app.route('/', methods=['GET', 'POST'])
def homepage():

    if request.method == 'POST':
        return homepage_agent.post()
    elif request.method == 'GET':
        return homepage_agent.get()

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        
        return login_agent.post()
    elif request.method == 'GET':
        return login_agent.get()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return register_agent.post()
    elif request.method == 'GET':
        return register_agent.get()

#@app.route('/register/confirm/<token>')
#def confirm_email(token):
#    email = safe_timed_url_serializer.loads(token, max_age=60)
#    return 'the token works'

if __name__ == '__main__':
    app.run(debug=True)

