from app.app import app
from src.app.homepage.homepage import HomePage
from src.app.login.login import Login
from flask import request


homepage_agent = HomePage()
login_agent = Login()

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
    return {'hola' : 'register'}

if __name__ == '__main__':
    app.run(debug=True)