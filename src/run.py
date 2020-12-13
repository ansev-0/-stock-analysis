from src.app.app import app
from src.app.homepage.homepage import HomePage
from src.app.login.login import Login
from src.app.register.register import Register
from src.app.register.register_confirmed import RegisterConfirmed
from flask import request, session
from src.app import config
from datetime import timedelta



homepage_agent = HomePage()
login_agent = Login()
register_confirmed = RegisterConfirmed()
register_agent = Register(app)

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

@app.route('/register/confirm/<token>')
def confirm_email(token):
    return register_confirmed(token) if register_agent.validate_register(token) else 'the token does not work!'

@app.route('/waiting/confirm')
def successful_register():
    return {'waiting' : 'confirm'}

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=5)

if __name__ == '__main__':
    app.config.from_object('src.app.config.DeveloperConfig')
    app.run(debug=True)
